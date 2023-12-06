from database.Database import Database
from database.Faq import Faq

class FaqService():
    @staticmethod
    def get_all_faq() -> list:
        """
        Récupérer toute la FAQ
        """
        faqDb: Faq = Database.get_table("faq")
        response = faqDb.fetchall()
        faqDb.close()
        return response
    
    @staticmethod
    def add_faq(question: str, answer: str) -> bool:
        """
        Ajouter une question et une réponse dans la FAQ
        """
        faqDb: Faq = Database.get_table("faq")
        response = faqDb.insert(question, answer)
        faqDb.close()
        return response
    
    @staticmethod
    def remove_faq(id: int) -> bool:
        """
        Supprimer une question et une réponse de la FAQ par son ID
        """
        faqDb: Faq = Database.get_table("faq")
        response = faqDb.remove(id)
        faqDb.close()
        return response