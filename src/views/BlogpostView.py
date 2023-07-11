from flask import request, json, Response, Blueprint,g
from marshmallow import ValidationError
from ..models.BlogpostModel import BlogpostModel, BlogpostSchema
from ..shared.Authentication import Auth


blogpost_api = Blueprint('blogpost_api', __name__)
blogpost_schema = BlogpostSchema()

@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Blogpost Function
    """

    req_data = request.get_json()
    req_data["owner_id"] = g.user.get('id')
    # print(req_data)
    try:
        data = blogpost_schema.load(req_data, partial=True)
        post = BlogpostModel(data)
        post.save()
    except ValidationError:
        return custom_response({'error': "Incorrect Data Format"}, 400)
    
    data = blogpost_schema.dump(post)
    return custom_response(data, 201)


@blogpost_api.route('/', methods=['GET'])
def get_all():
    """
    Get All blogposts
    """

    posts = BlogpostModel.get_all_blogposts()
    data = blogpost_schema.dump(posts, many=True)
    return custom_response(data, 200)




def custom_response(res, status_code):
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )

@blogpost_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one(blogpost_id):
    """
    Get A Single blogpost
    """
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    
    data = blogpost_schema.dump(post)
    return custom_response(data, 200)

@blogpost_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
    """
    Update A blogpost
    
    """

    req_data = request.get_json()
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    if data.get("owner_id") != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    try:
        data = blogpost_schema.load(req_data, partial=True)
        post.update(data)
    except ValidationError:
        return custom_response({'error': "Incorrect Data Format"}, 400)
    
    data = blogpost_schema.dump(post)
    return custom_response(data, 200)




@blogpost_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete(blogpost_id):
    post = BlogpostModel.get_one_blogpost(blogpost_id)
    if not post:
        return custom_response({'error': 'post not found'}, 404)
    data = blogpost_schema.dump(post)
    if data.get("owner_id") != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)
    
    try:
        post.delete()
    except:
        custom_response({'error': 'Server issue'}, 400)

    return custom_response({'message': 'deleted'}, 200)

     