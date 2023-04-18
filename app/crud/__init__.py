from app.crud.rss_posts import rss_posts_methods
from app.crud.rss_sources import rss_sources_methods
from app.crud.vk_groups import vk_group_methods
from app.crud.vk_usertokens import vk_usertoken_methods


class CRUD:
    vk_group_methods = vk_group_methods
    rss_posts_methods = rss_posts_methods
    rss_sources_methods = rss_sources_methods
    vk_usertoken_methods = vk_usertoken_methods
