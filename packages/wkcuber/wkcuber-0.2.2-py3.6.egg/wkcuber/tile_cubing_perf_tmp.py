import time
import logging
import numpy as np
import re
import wkw
from argparse import ArgumentParser
from os import path, listdir
from PIL import Image

from .utils import (
    get_chunks,
    get_regular_chunks,
    find_files,
    add_verbose_flag,
    add_jobs_flag,
    pool_get_lock,
    open_wkw,
    WkwDatasetInfo,
    ParallelExecutor,
)
from .cubing import create_parser, read_image_file
from .image_readers import image_reader

BLOCK_LEN = 32
CUBE_REGEX = re.compile("(\d+)/(\d+)\.([a-zA-Z]{3,4})$")


def find_source_sections(source_path):
    section_folders = [
        f for f in listdir(source_path) if path.isdir(path.join(source_path, f))
    ]
    section_folders = [path.join(source_path, s) for s in section_folders]
    section_folders.sort()
    return section_folders


def parse_tile_file_name(filename):
    m = CUBE_REGEX.search(filename)
    if m is None:
        return None
    return (int(m.group(1)), int(m.group(2)), m.group(3))


def find_source_files(source_section_path):
    all_source_files = [
        path.join(source_section_path, s)
        for s in find_files(
            path.join(source_section_path, "**", "*"), image_reader.readers.keys()
        )
    ]

    all_source_files.sort()
    return all_source_files


def tile_cubing_job(target_wkw_info, z_batches, source_path, batch_size, tile_size, num_channels):
    if len(z_batches) == 0:
        return

    with open_wkw(target_wkw_info, pool_get_lock()) as target_wkw:
        # Iterate over the z batches
        # Batching is useful to utilize IO more efficiently
        for z_batch in get_chunks(z_batches, batch_size):
            try:
                ref_time = time.time()
                logging.info("Cubing z={}-{}".format(z_batch[0], z_batch[-1]))

                # Detect all available tiles in this z batch
                tile_coords = []
                for z in z_batch:
                    tile_coords += [
                        (z,) + parse_tile_file_name(f)
                        for f in find_source_files("{}/{}".format(source_path, z))
                    ]
                # Figure out what x-y combinations are available in this z batch
                xy = sorted(set([(x, y) for z, y, x, _ in tile_coords]))

                # Iterate over all x-y combinations from this z batch
                for x, y in xy:
                    print("next xy tile", x, y)
                    ref_time2 = time.time()
                    is_multi_channel = num_channels > 1

                    z_batch_len = 4 len(z_batch)
                    buffer_shape = (tile_size[0], tile_size[1], num_channels * z_batch_len)
                    print("allocating shape", buffer_shape)
                    buffer = np.empty(buffer_shape, target_wkw_info.dtype)
                    for idx, z in enumerate(z_batch):
                        # Find the file extension of the x-y tile in this z
                        ext = next(
                            (
                                ext
                                for _z, _y, _x, ext in tile_coords
                                if _z == z and _y == y and _x == x
                            ),
                            None,
                        )

                        if z == z_batch_len:
                            break

                        # Determine the region within the buffer, the tile should be written to.
                        # Using the tile index as the first dimension, yields a benefit of
                        # approximately factor 2.
                        def write_tile(tile_image):
                            if is_multi_channel:
                                target = buffer[:, :, idx * num_channels : (idx + 1) * num_channels]
                            else:
                                buffer[:, :, idx] = tile_image

                        # Read file if exists or zeros instead
                        if ext is not None:
                            print("writing to target with shape", " -- ", idx, z)
                            write_tile(np.squeeze(read_image_file(
                                                            "{}/{}/{}/{}.{}".format(source_path, z, y, x, ext),
                                                            target_wkw_info.dtype,
                                                        )))
                            print("buffer[idx, :, :] != 0", np.any(buffer[:, :, idx] != 0))
                        else:
                            write_tile(np.zeros(tile_size, dtype=target_wkw_info.dtype))

                    # Write buffer to target
                    if np.any(buffer != 0):
                        print("transpose")
                        # Transpose the buffer back so that z is in the third dimension.
                        # buffer = np.transpose(buffer, (1, 2, 0))
                        print("write to wkw")
                        target_wkw.write(
                            [x * tile_size[0], y * tile_size[1], z_batch[0]], buffer
                        )
                    else:
                        print("buffer is empty")
                    logging.debug(
                        "Cubing of z={}-{} x={} y={} took {:.8f}s".format(
                            z_batch[0], z_batch[-1], x, y, time.time() - ref_time2
                        )
                    )

                logging.debug(
                    "Cubing of z={}-{} took {:.8f}s".format(
                        z_batch[0], z_batch[-1], time.time() - ref_time
                    )
                )

            except Exception as exc:
                logging.error(
                    "Cubing of z={}-{} failed with {}".format(
                        z_batch[0], z_batch[-1], exc
                    )
                )
                raise exc


def tile_cubing(source_path, target_path, layer_name, dtype, batch_size, jobs):
    # Detect available z sections
    sections = find_source_sections(source_path)
    if len(sections) == 0:
        logging.error("No source files found")
        return
    min_z = min([int(path.basename(f)) for f in sections])
    max_z = max([int(path.basename(f)) for f in sections])

    # Determine tile size from first matching file
    sample_tile = next(find_files(path.join(source_path, "**", "*"), image_reader.readers.keys()))
    tile_size = image_reader.read_dimensions(sample_tile)
    num_channels = image_reader.read_channel_count(sample_tile)
    logging.info(
        "Found source files: count={} tile_size={}x{}".format(
            len(sections), tile_size[0], tile_size[1]
        )
    )

    target_wkw_info = WkwDatasetInfo(target_path, layer_name, dtype, 1)
    # with ParallelExecutor(jobs) as pool:
        # Iterate over all z batches
    for z_batch in get_regular_chunks(min_z, max_z, BLOCK_LEN):
        # pool.submit(
        tile_cubing_job(
            target_wkw_info,
            list(z_batch),
            source_path,
            int(batch_size),
            tile_size,
            num_channels,
        )
        return


if __name__ == "__main__":
    args = create_parser().parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    tile_cubing(
        args.source_path,
        args.target_path,
        args.layer_name,
        args.dtype,
        int(args.batch_size),
        int(args.jobs),
    )
