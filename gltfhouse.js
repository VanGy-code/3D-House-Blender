const obj2gltf = require("obj2gltf");
const fs = require("fs");
const data_dir = 'C:/Project/Datasets/3D-FRONT/';
const house_id = '0f2bcc07-85c2-41a1-8712-cee71117aff6';

const house_info = fs.readFileSync( data_dir + 'house/' + house_id + '/house.json', 'utf8').replace(/\bNaN\b/g, "null")
const house_config = JSON.parse(house_info);
const dir = './scenes/' + house_id + '/';

if(!fs.existsSync(dir)){
    fs.mkdirSync(dir);
}
let obj_to_gltf = function(obj_path, gltf_path){
    obj_path = obj_path + '.obj';
    gltf_path = gltf_path + '.gltf';
    if(!fs.existsSync(obj_path)){
        console.log(obj_path + ': does not exist! ');
        return
    }
    obj2gltf(obj_path)
        .then(function(gltf) {
            const data = Buffer.from(JSON.stringify(gltf));
            fs.writeFileSync(gltf_path, data);
        });
};

house_config.levels.forEach(function(level){
   let nodes = level.nodes;
   nodes.forEach(function(node){
       console.log(node.modelId);
       if(node.type === 'Room'){
           let fname = node.modelId + 'c';
           // copy_obj(dir + fname, data_dir + 'room/' + house_id + '/' + fname);
           obj_to_gltf(data_dir + 'room/' + house_id + '/' + fname, dir + fname);
           fname = node.modelId + 'f';
           obj_to_gltf(data_dir + 'room/' + house_id + '/' + fname, dir + fname);
           // copy_obj(dir + fname, data_dir + 'room/' + house_id + '/' + fname);
           fname = node.modelId + 'w';
           obj_to_gltf(data_dir + 'room/' + house_id + '/' + fname, dir + fname);
           // copy_obj(dir + fname, data_dir + 'room/' + house_id + '/' + fname);
       }else if(node.type === 'Object'){
           let fname = node.modelId;
           // copy_obj( dir + fname, data_dir + 'object/' + fname + '/' + fname)
           obj_to_gltf(data_dir + 'object/' + fname + '/' + fname, dir + fname);
       }else if(node.type === 'Ground'){
           let fname = node.modelId + 'f';
           // copy_obj( dir + fname, data_dir + 'room/' + fname + '/' + fname)
           obj_to_gltf(data_dir + 'room/' + house_id + '/' + fname, dir + fname);
       }
   })
});
fs.readFile(data_dir + 'house/' + house_id + '/house.json', function (err, data) {
    if (err){
        throw err;
    }
    fs.writeFile(dir + 'house.json', data, function (err) {
        if (err){
            throw err;
        }
        console.log("House.json file was saved! ");
    })
});
