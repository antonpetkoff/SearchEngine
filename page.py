from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from connection import Base


class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    desc = Column(String)
    SSL = Column(Boolean)
    multilang = Column(Integer)
    points = Column(Integer)

    website_id = Column(Integer, ForeignKey("website.id"))
    website = relationship("Website", backref="pages")

    def __str__(self):
        msg = "id({}), url({}), title({}), desc({}), "
        msg += "SSL({}), multilang({}), points({})"
        return msg.format(self.id, self.url, self.title, self.desc,
                          self.SSL, self.multilang. self.points)

    def __repr__(self):
        return self.__str__()
