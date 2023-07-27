from urllib import response
from datetime import datetime
from database.Database import Database
from database.AccountDetails import AccountDetails
from database.Account import AccountDatabase
from services.utils.GenerateAuthenticator import GenerateAuthenticator
from database.Faq import Faq
import pyotp

class FaqService():
    @staticmethod
    def get_all_faq() -> list:
        faqDb: Faq = Database.get_table("faq")
        response = faqDb.fetch_all()
        faqDb.close()
        return response
    
    @staticmethod
    def add_faq(question: str, answer: str) -> bool:
        faqDb: Faq = Database.get_table("faq")
        response = faqDb.insert(question, answer)
        faqDb.close()
        return response
    
    @staticmethod
    def remove_faq(id: int) -> bool:
        faqDb: Faq = Database.get_table("faq")
        response = faqDb.remove(id)
        faqDb.close()
        return response