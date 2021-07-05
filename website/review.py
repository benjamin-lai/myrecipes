# This is contains helper functions to create, modify and delete messages.
from flask import Blueprint, request, flash, jsonify
import json

from .models import Comments
from . import db

review = Blueprint('review', __name__)

# Creates a comment given the recipe_id
# Already checks http request 
def create_comment(recipe_id):
    comment = request.form.get('review')
    print(recipe_id)
    print(comment)

    if len(comment) < 1:
        flash('Comment is too short!', category='error')
    else:
        new_comment = Comments(comment=comment, has=recipe_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', category='success')

# Retrieves comments given recipe_id
def retrieve_comments(recipe_id):
    return Comments.query.filter_by(has = recipe_id).all()

@review.route('/delete-comment', methods=['POST'])
def delete_comment():
    comment = json.loads(request.data)
    comment_id = comment['comment_id']
    comment = Comments.query.get(comment_id)
    print(comment)
    db.session.delete(comment)
    db.session.commit()

    return jsonify({})
