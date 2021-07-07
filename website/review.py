# This is contains helper functions to create, modify and delete messages.
from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
import json

from .models import Comments, Profiles, Likes, Recipes
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
            profile = Profiles.query.filter_by(owns=current_user.id).first()
            print(profile.display_name)
            new_comment = Comments(comment=comment, has=recipe_id, owns=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added!', category='success')
        return jsonify({})

# Retrieves comments given recipe_id
def retrieve_comments(recipe_id):
    # Create a list that stores both the display_name of comment creator and comments themselves.
    name_and_list_comments = []
    list_comments = Comments.query.filter_by(has = recipe_id).all()
    for comments in list_comments:
        # Instead of adding display name to comments table, we find it here given comments.own
        # Creates a lot of overhead right now, needs to be fixed later
        profile = Profiles.query.filter_by(owns=comments.owns).first()
        name_and_comment = (profile.display_name, comments)
        name_and_list_comments.append(name_and_comment)
    return name_and_list_comments

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


@review.route('/add-like', methods=['POST'])
def add_like():
    if current_user.is_authenticated:
        # If user is going through this path it means they have clicked like
        # Which should imply that status = 1.
        status = 1
        like_dislike_recipe(status)

    else:
        flash("You need to be logged in to do that", category='error')

    return jsonify({})

@review.route('/add-dislike', methods=['POST'])
def add_dislike():
    if current_user.is_authenticated:
        # If user is going through this path it means they have clicked like
        # Which should imply that status = -1.
        status = -1
        like_dislike_recipe(status)

    else:
        flash("You need to be logged in to do that", category='error')
    
    return jsonify({})

# Process to either like or dislike recipe given the status
def like_dislike_recipe(status):
    recipe = json.loads(request.data)
    recipe_id = recipe['recipe_id']
    recipe = Recipes.query.filter_by(id=recipe_id).first()

    # Determine if there is a like table for this user and recipe already
    likes_table = check_likes_exists(current_user.id, recipe.id)
    if likes_table is not None: 
        # Update like
        update_like_status(recipe, status, likes_table)
    else:   # If like_table doesn't exist
        # Create like table and assign the correct status
        create_likes_table(status, recipe, current_user.id)


# Helper function for likes/dislikes
def create_likes_table(status, recipe, user_id):
    # Create new likes table for the user
    new_likes = Likes(like_status=status, has=recipe.id, own=user_id)

    # Update count for recipe
    if status == 1:
        recipe.num_of_likes += 1
    else:
        recipe.num_of_dislikes += 1
    
    db.session.add(new_likes)
    db.session.commit()

# Checks if table already exists for the user
def check_likes_exists(user_id, recipe_id):
    return Likes.query.filter_by(own=user_id, has=recipe_id).first()

# Updates recipe like/dislike count.
# New status can only be 1 (liked) or -1 (dislike).
def update_like_status(recipe, new_status, likes):
    current_status = likes.like_status

    if current_status == 0:                     # User has not liked/disliked
        if new_status == 1:                     # User has selected like
            recipe.num_of_likes += 1            # Iterate like count by 1
        else:                                   # User has selected dislike
            recipe.num_of_dislikes += 1         # Iterate dislike count by 1
        likes.like_status = new_status          # Updated like_status to new_status

    elif current_status == 1:                   # User has liked before
        recipe.num_of_likes -= 1                # Decrease number of likes by 1
        if new_status == 1:                     # User has selected like again
            likes.like_status = 0               # Change like status to nothing
        else:                                   # User has selected dislike
            likes.like_status = new_status      # Update like_status to new_status
            recipe.num_of_dislikes += 1         # Update number of dislikes

    else:                                       # User has disliked before
        recipe.num_of_dislikes -= 1             # Decrease number of likes by 1
        if new_status == 1:                     # User has selected like again
            likes.like_status = new_status      # Change like status to nothing
            recipe.num_of_likes += 1            # Update number of likes
        else:                                   # User has selected dislike
            likes.like_status = 0               # Update like_status to new_status

    db.session.commit()

    