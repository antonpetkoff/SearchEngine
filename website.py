from sqlalchemy import Column, Integer, String, Boolean
from connection import Base


class Website(Base):
    __tablename__ = "website"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    domain = Column(String)
    pages_count = Column(Integer)
    is_html_5 = Column(Boolean)

    def __str__(self):
        msg = "id({}), url({}), title({}), domain({}), "
        msg += "pages_count({}), is_html_5({})"
        return msg.format(self.id, self.url, self.title, self.domain,
                          self.pages_count, self.is_html_5)

    def __repr__(self):
        return self.__str__()
