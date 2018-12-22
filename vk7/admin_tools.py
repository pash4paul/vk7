# coding: utf8

from vk7 import Vk


class AdminTools(Vk):
    def clean_wall(self, owner_id):
        for post in self.wall.get(owner_id=owner_id):
            self.wall.delete(owner_id=owner_id, post_id=post['id'])

    def copy_post_to_owner_wall(self, post_id, owner_id):
        post = self.wall.getById(posts=post_id)['response'][0]

        def convert_attachment(attachment):
            a_type = attachment['type']
            return '{}{}_{}'.format(a_type, attachment[a_type]['owner_id'], attachment[a_type]['id'])

        attachments = [convert_attachment(attachment) for attachment in post['attachments']]

        return self.wall.post(owner_id=owner_id, message=post['text'], attachments=','.join(attachments))
