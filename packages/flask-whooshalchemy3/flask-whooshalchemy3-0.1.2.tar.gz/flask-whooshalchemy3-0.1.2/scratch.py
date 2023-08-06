#! /usr/bin/env python
# -*- coding: utf-8 -*-
# >>
#     Flask-WhooshAlchemy3, 2017
# <<

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy

from whoosh.analysis import StemmingAnalyzer
app = Flask(__name__)

db = SQLAlchemy()


class PACKTPUB(db.Model):
    __tablename__ = "packtpubs"
    # these fields will be indexed by whoosh
    __searchable__ = ['title', 'isbn']
    _analyzer__ = StemmingAnalyzer()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    isbn = db.Column(db.String(50), index=True, unique=True)

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn

    def __repr__(self):
        return '<PacktPub Title %r>' % (self.title)


@app.route('/packtpubs/search')
def search():
    num_posts = 10
    query = request.args.get('q', '')
    results = PACKTPUB.query.search(query, limit=num_posts)
    results = ', '.join(map(str, results))
    return results


@app.route('/packtpubs/create', methods=['POST'])
def packtpubs_create():
    j = request.get_json()

    packtpub = PACKTPUB(
        title=request.get_json().get('title'),
        isbn=request.get_json().get('isbn')
    )
    db.session.add(packtpub)
    db.session.commit()
    return 'DONE'


@app.before_first_request
def bootstrap():
    db.create_all()
    flask_whooshalchemy.search_index(app, PACKTPUB)


if __name__ == "__main__":
    db.init_app(app)
    app.run()


