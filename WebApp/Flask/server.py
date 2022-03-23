from flask import Flask, Response, request, jsonify, send_from_directory
import json
from serialization import json_custom


HOST = 'localhost'
PORT = 8000
UI_BUILD_DIR = "../UI/build"

app = Flask(__name__, static_url_path="/", static_folder=UI_BUILD_DIR)

def create_response(status_code:int) -> Response:

    status_text_dict = {
        200:"OK",
        204: "No Content",
        302: "Found",
        401:"Unauthorized",
        404:"not found",
        409:"conflict",
        500:"internal server error"
    }
    status_text = status_text_dict[status_code]

    return Response(status_text,status_code)




@app.route('/')
def index():
    return send_from_directory(UI_BUILD_DIR, 'index.html')

@app.route("/samples")
def samples_index():
    import samples
    return json.dumps(samples.SAMPLES)

@app.route("/compile", methods=["POST"])
def compile_request():
    data = str(request.data, 'utf-8')

    import parser
    statements = parser.parse_free_text(data)
    for s in statements:
        print(s)

    result = {"statements": statements}

    return json_custom(result)

def _get_points_coordinates(point_name, all_points):
    assert(point_name in all_points)
    return all_points[point_name]

def get_output(input_text):
    # Get input from the user, return the partial program, the output points and output lines\rays\segments
    statements = parser.parse_free_text(input_text)
    partial_prog = synthesis.main(exercise_name=exercise_name, statements=statements)
    print("Partial program is: ")
    print(partial_prog)
    print("Perform numeric search")
    results = hillClimbing.hillClimbing(partial_prog.known, partial_prog.rules, not_equal=partial_prog.not_equal_rules, not_in=partial_prog.not_in_rules, not_collinear=partial_prog.not_colinear, not_intersect_2_segments=partial_prog.not_intersect_2_segments)
    print("numeric search results are: ")
    print(results)
    # Get the output points
    out_points = {}
    # Results is a dictionary
    for var_name, val in results.items():
        if is_point(val):
            out_points[var_name] = (val.x, val.y)
            
    # Get segments and circles to draw
    # draw only draw_circle\draw_segment statements
    # Get the points coordinates from the hill climbing results
    out_lines = []
    for s in statements:
        if s.predicate == "drawSegment":
            # Format for segment: (a.x, a.y, b.x, b.y)
            point_a = s.vars[0]
            point_b = s.vars[0]
            segment_ab = (*_get_points_coordinates(point_a, out_points), 
            *_get_points_coordinates(point_b, out_points))
            out_lines.append(segment_ab)
        if s.predicate == "draw_circle":
            # Format for circle: (a.x, a.y, r)
            point_a = s.vars[0]
            radius = s.vars[1]
            circle_a = (*_get_points_coordinates(point_a, out_points), radius)
            out_lines.append(circle_a)
    
    output = namedtuple("output", "partial_prog output_points output_lines")
    return output(str(partial_prog), out_points, out_lines)

@app.route("/solve", methods=["POST"])
def solve_request():
    data = str(request.data, 'utf-8')

    print("TODO invoke solver on data", data)

    result = {}

    return json_custom(result)


# @app.route('/add_reply/', methods=['GET'])
# def addReply():
#     try:
#         id = request.args.get('userTelegramID')
#         answer = request.args.get('Answer')
#         pollID = request.args.get('PollID')
#         status_code = updateReplyInDB(id, answer, pollID)
#         return create_response(status_code)
#     except:
#         return create_response(status_code=500)
#
#
# @app.route('/get_all_admins/', methods=['POST'])
# def getAllAdmins():
#     try:
#         body = request.get_json()
#         status_code = isAdminRegistered(body['username'], body['password'])
#         if status_code == 500:
#             return create_response(status_code)
#         elif status_code != 200:
#             return create_response(401)
#
#         status_code, admins = getAllAdminsFromDB()
#
#         if status_code == 500:
#             raise
#
#         return jsonify({"admins": admins})
#     except:
#         return create_response(status_code=500)



# ---------------------------static functions--------------------------------#


if __name__ == '__main__':
    app.run(debug=True, port=PORT, host=HOST)



