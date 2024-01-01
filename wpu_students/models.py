from sqlalchemy import Integer, String, DateTime, Boolean, Text, ForeignKey, func
import datetime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from . import db


class User(db.Model):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20),
                                          unique=True,
                                          nullable=False)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True),
                                            default=datetime.now)
    is_activated: Mapped[bool] = mapped_column(Boolean,
                                               default=False,
                                               nullable=False)
    role: Mapped[str] = mapped_column(String(10),
                                      nullable=False,
                                      default='user')
    receipts = relationship('Receipt', backref=backref('users'))

    def __repr__(self) -> str:
        return f'User(username="{self.username}", fullname="{self.fullname}", is_activated="{self.is_activated}", role="{self.role}")'


class Faculty(db.Model):

    __tablename__ = 'faculties'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    receipts = relationship('Receipt', backref=backref('faculties'))

    def __repr__(self) -> str:
        return f'Faculty(title="{self.title}")'


class Service(db.Model):

    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    receipts = relationship('ReceiptDetail', backref=backref('services'))

    def __repr__(self) -> str:
        return f'Service(name="{self.name}", price={self.price:,})'


class Receipt(db.Model):

    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 nullable=False,
                                                 default=func.now())
    date: Mapped[datetime.date] = mapped_column(DateTime,
                                                nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    client: Mapped[str] = mapped_column(String(50), nullable=False)
    client_id: Mapped[str] = mapped_column(String(50), nullable=True)
    faculty_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("faculties.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)

    receipts = relationship('ReceiptDetail', backref=backref('receipts'))

    def __repr__(self) -> str:
        return f"Receipt(id='{self.id}', client='{self.client}')"


class ReceiptDetail(db.Model):

    __tablename__ = 'receipts_details'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('services.id'), nullable=False)
    receipt_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('receipts.id'), nullable=False)

    def __repr__(self) -> str:
        return f'ReceiptDetails(service_id="{self.service_id}", quantity="{self.quantity}", price="{self.price}")'
