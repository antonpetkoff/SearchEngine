from sqlalchemy.orm import Session
from connection import Base
from connection import engine
from page import Page
from website import Website


class SearchEngine:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)

    def make_query(self, query):
        results = self.session.query(Page).\
            filter(Page.title.like('%' + query + '%')).\
            order_by(Page.score.desc()).all()
        return results


def main():
    se = SearchEngine()
    print(se.make_query('Anto'))


if __name__ == '__main__':
    main()
