# coding: utf8

from typing import Generator

from vk7 import VK
from vk7.data_iterators import group_members_iterator, group_posts_iterator


def deactivated_members_iterator(vk: VK, group_id: int,
                                 deactivated_types: str='deleted,banned',
                                 verbose: bool=False) -> Generator:

    deactivated_types = deactivated_types.split(',')

    for member in group_members_iterator(vk, group_id, verbose=verbose):
        if member.get('deactivated') in deactivated_types:
            yield member


def members_without_photo_iterator(vk: VK, group_id: int,
                                   verbose: bool=False) -> Generator:

    for member in group_members_iterator(vk, group_id, fields='has_photo',
                                         verbose=verbose):
        if (
                not member.get('has_photo', 0)
                and member.get('deactivated') not in ('deleted', 'banned')
        ):
            yield member


def clean_wall(vk: VK, group_id: int, verbose: bool=False):
    for post in group_posts_iterator(vk, group_id, verbose):
        vk.wall.delete(owner_id='-{}'.format(group_id), post_id=post['id'])


def copy_post_to_wall(vk: VK, post_id: str, wall_group_id: int):
    post = vk.wall.getById(posts=post_id)['response'][0]

    attachments = []
    for attachment in post['attachments']:
        attachment_type = attachment['type']
        owner_id = attachment[attachment_type]['owner_id']
        media_id = attachment[attachment_type]['id']
        attachments.append('{}{}_{}'.format(
            attachment_type, owner_id, media_id)
        )

    return vk.wall.post(
        owner_id='-{}'.format(wall_group_id), message=post['text'],
        attachments=','.join(attachments)
    )
