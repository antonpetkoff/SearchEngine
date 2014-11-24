from sqlalchemy import Column, Integer, String
from connection import Base


class Website(Base):
    __tablename__ = "website"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    domain = Column(String)
    pages_count = Column(Integer)
    HTML_ver = Column(String)

    def __str__(self):
        msg = "id({}), url({}), title({}), domain({}), "
        msg += "pages_count({}), HTML_ver({})"
        return msg.format(self.id, self.url, self.title, self.domain,
                          self.pages_count, self.HTML_ver)

    def __repr__(self):
        return self.__str__()
