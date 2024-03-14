import glob
import os
import shutil

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    dataset_path = "/home/alex/DATASETS/TODO/CholecSeg8k/archive"
    batch_size = 30
    ds_name = "ds"

    masks_suffix = "_color_mask.png"

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors

    def create_ann(image_path):
        labels = []

        mask_path = image_path.replace("_endo.png", "_endo_color_mask.png")

        video_id, seq_id = image_path.split("/")[-2].split("_")

        video = sly.Tag(video_meta, value=int(video_id[6:]))
        seq = sly.Tag(seq_meta, value=int(seq_id))

        mask_np = sly.imaging.image.read(mask_path)
        img_height = mask_np.shape[0]
        img_wight = mask_np.shape[1]
        unique_colors = get_unique_colors(mask_np)
        for color in unique_colors:
            mask = np.all(mask_np == color, axis=2)
            bitmap = sly.Bitmap(data=mask)
            obj_class = color_to_obj_class.get(color)
            if obj_class is None:
                continue
            label = sly.Label(bitmap, obj_class)
            labels.append(label)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[video, seq]
        )

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    from supervisely.imaging.color import hex2rgb

    class_to_color = {
        "black background": (0, 0, 0),
        "Abdominal Wall": (210, 140, 140),
        "Liver": (255, 114, 114),
        "Gastrointestinal Tract": (231, 70, 156),
        "Fat": (186, 183, 75),
        "Grasper": (170, 255, 0),
        "Connective Tissue": (255, 85, 0),
        "Blood": (255, 0, 0),
        "Cystic Duct": (255, 255, 0),
        "L-hook Electrocautery": (169, 255, 184),
        "Gallbladder": (255, 160, 165),
        "Hepatic Vein": (0, 50, 128),
        "Liver Ligament": (111, 74, 0),
    }

    video_meta = sly.TagMeta("video id", sly.TagValueType.ANY_NUMBER)
    seq_meta = sly.TagMeta("sequence", sly.TagValueType.ANY_NUMBER)

    meta = sly.ProjectMeta(tag_metas=[video_meta, seq_meta])
    color_to_obj_class = {}

    for class_name, color in class_to_color.items():
        obj_class = sly.ObjClass(class_name.lower(), sly.Bitmap, color=color)
        color_to_obj_class[tuple(color)] = obj_class
        meta = meta.add_obj_class(obj_class)

    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = [
        im_path
        for im_path in glob.glob(dataset_path + "/*/*/*.png")
        if get_file_name_with_ext(im_path)[-8:] == "endo.png"
    ]

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [
            im_path.split("/")[-3] + "_" + get_file_name_with_ext(im_path)
            for im_path in img_pathes_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    return project
