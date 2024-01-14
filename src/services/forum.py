from datetime import datetime
import json
from database.CompletedTutorials import CompletedTutorials
from database.Paths import Paths
from database.Tutorials import Tutorials
from database.Category import Category
from database.UserTutorialScore import UserTutorialScore
from database.Database import Database
from database.Account import AccountDatabase
from database.ForumPosts import ForumPosts
from database.ForumComments import ForumComments

from typing import Dict
import os
import requests
import base64


class ForumService:
    @staticmethod
    def get_all_posts() -> list:
        """
        Récupérer la liste des tutoriels
        """
        forumPostDb: ForumPosts = Database.get_table("ForumPosts")

        posts = forumPostDb.fetch_all()
        print(posts)
        post_list = []
        if len(posts) > 0:
            for post in posts:
                post_list.append(
                    {
                        "id": post["id"],
                        "title": post["title"],
                        "category": post["category"],
                        "description": post["description"],
                        "image": post["image"],
                        "points": post["points"],
                        "author_uuid": post["author_uuid"]
                        # "time_created": post["time_created"],
                    }
                )
        else:
            forumPostDb.close()
            return []
        forumPostDb.close()
        return post_list
    
    @staticmethod
    def get_all_comments_post(post_id:int) -> list:
        """
        Recuperer tout les commentaires d'un post
        """
        forumPostDb: ForumComments = Database.get_table("ForumComments")

        comments = forumPostDb.fetch(post_id)
        print("ALL COMMENTS", comments)
        comments_list = []
        if len(comments) > 0:
            for post in comments:
                comments_list.append(
                    {
                        "post_id": post["post_id"],
                        "author_uuid": post["author_uuid"],
                        "text": post["text"]
                    }
                )
        else:
            forumPostDb.close()
            return []
        forumPostDb.close()
        return comments_list
        

    @staticmethod
    def create_post(title: str, author_uuid: int, description: str, points: int, category: str, image:str) -> bool:
        """
        Créer un article
        """
        forumPostDb: ForumPosts = Database.get_table("ForumPosts")
        success = forumPostDb.insert(title, author_uuid, description, points, category, image)
        print(success)
        forumPostDb.close()
        return success
    