
@file.route('/prepare_for_jsonify', methods=['GET', 'POST'])
def prepare_for_jsonify(filles):

    print("")
    print("")
    print("IN jsonify_fies")
    
    files_arr = []
    for f in files:
        tmp_arr = {}   #JSON STYLE
            print("SUB: ", f.id, f.name)
            print("")
            tmp_arr['name'] = f.name
            tmp_arr['body'] = f.body
            tmp_arr['data'] = f.data
            files_arr.append(tmp_arr)
            
    print("")
    print("")
    print("IN sub_tag ")
    print("files_arr: ", files_arr)
        
    #return jsonify({'FILES': files_arr})    
    return files_arr    
