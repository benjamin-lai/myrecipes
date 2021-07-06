# This is contains helper functions to create, modify and delete messages.
from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
import json

from .models import Comments, Recipes
from . import db

review = Blueprint('review', __name__)

# Creates a comment given the recipe_id
# Already checks http request 
@review.route('/create-comment', methods=['POST'])
@login_required
def create_comment():
    if request.method == 'POST':
        recipe = json.loads(request.data)
        recipe_id = recipe['recipe_id']
        comment = recipe['comment']

        if len(comment) < 1:
            flash('Comment is too short!', category='error')
        else:
            print(current_user.id)
            new_comment = Comments(comment=comment, has=recipe_id, owns=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', category='success')
        return jsonify({})

# Retrieves comments given recipe_id
def retrieve_comments(recipe_id):
    return Comments.query.filter_by(has = recipe_id).all()

@review.route('/delete-comment', methods=['POST'])
def delete_comment():
    if request.method == 'POST':
        comment = json.loads(request.data)
        comment_id = comment['comment_id']
        comment = Comments.query.get(comment_id)

        db.session.delete(comment)
        db.session.commit()
        flash('Deleted comment successfully!', category='success')

        return jsonify({})

@review.route('/modify-comment', methods=['POST'])
def modify_comment():
    if request.method == 'POST':
        comment = json.loads(request.data)
        comment_id = comment['comment_id']
        new_comment = comment['comment']


        if len(new_comment) < 1:    
            flash('Comment is too short!', category='error')
        else:
            comment = Comments.query.get(comment_id)
            comment.comment = new_comment
            db.session.commit()
            flash('Modified comment successfully!', category='success')

        return jsonify({})