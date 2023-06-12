from trimesh import util
from trimesh.constants import log
from trimesh.exchange.gltf import _data_append, _append_material, _build_accessor,_GL_TRIANGLES,_jsonify, uint32,uint8,float32

#Changed defnition of Trimesh's glb export to support multiple uv channels
def _append_multi_uv_mesh(mesh,
                 name,
                 tree,
                 buffer_items,
                 include_normals,
                 unitize_normals,
                 mat_hashes):
    """
    Append a mesh to the scene structure and put the
    data into buffer_items.

    Parameters
    -------------
    mesh : trimesh.Trimesh
      Source geometry
    name : str
      Name of geometry
    tree : dict
      Will be updated with data from mesh
    buffer_items
      Will have buffer appended with mesh data
    include_normals : bool
      Include vertex normals in export or not
    unitize_normals : bool
      Transform normals into unit vectors.
      May be undesirable but will fail validators without this.

    mat_hashes : dict
      Which materials have already been added
    """
    # return early from empty meshes to avoid crashing later
    if len(mesh.faces) == 0 or len(mesh.vertices) == 0:
        log.debug('skipping empty mesh!')
        return
    # convert mesh data to the correct dtypes
    # faces: 5125 is an unsigned 32 bit integer
    # accessors refer to data locations
    # mesh faces are stored as flat list of integers
    acc_face = _data_append(acc=tree['accessors'],
                            buff=buffer_items,
                            blob={"componentType": 5125,
                                  "type": "SCALAR"},
                            data=mesh.faces.astype(uint32))

    # vertices: 5126 is a float32
    # create or reuse an accessor for these vertices
    acc_vertex = _data_append(acc=tree['accessors'],
                              buff=buffer_items,
                              blob={"componentType": 5126,
                                    "type": "VEC3",
                                    "byteOffset": 0},
                              data=mesh.vertices.astype(float32))

    # meshes reference accessor indexes
    current = {"name": name,
               "extras": {},
               "primitives": [{
                   "attributes": {"POSITION": acc_vertex},
                   "indices": acc_face,
                   "mode": _GL_TRIANGLES}]}
    # if units are defined, store them as an extra
    # the GLTF spec says everything is implicit meters
    # we're not doing that as our unit conversions are expensive
    # although that might be better, implicit works for 3DXML
    # https://github.com/KhronosGroup/glTF/tree/master/extensions
    try:
        # skip jsonify any metadata, skipping internal keys
        current['extras'] = _jsonify(mesh.metadata)

        # extract extensions if any
        extensions = current['extras'].pop('gltf_extensions', None)
        if isinstance(extensions, dict):
            current['extensions'] = extensions

        if mesh.units not in [None, 'm', 'meters', 'meter']:
            current["extras"]["units"] = str(mesh.units)
    except BaseException:
        log.debug('metadata not serializable, dropping!',
                  exc_info=True)

    # check to see if we have vertex or face colors
    # or if a TextureVisual has colors included as an attribute
    if mesh.visual.kind in ['vertex', 'face']:
        vertex_colors = mesh.visual.vertex_colors
    elif (hasattr(mesh.visual, 'vertex_attributes') and
          'color' in mesh.visual.vertex_attributes):
        vertex_colors = mesh.visual.vertex_attributes['color']
    else:
        vertex_colors = None

    if vertex_colors is not None:
        # convert color data to bytes and append
        acc_color = _data_append(
            acc=tree['accessors'],
            buff=buffer_items,
            blob={"componentType": 5121,
                  "normalized": True,
                  "type": "VEC4",
                  "byteOffset": 0},
            data=vertex_colors.astype(uint8))

        # add the reference for vertex color
        current["primitives"][0]["attributes"][
            "COLOR_0"] = acc_color

    if hasattr(mesh.visual, 'material'):
        # append the material and then set from returned index
        current_material = _append_material(
            mat=mesh.visual.material,
            tree=tree,
            buffer_items=buffer_items,
            mat_hashes=mat_hashes)

        # if mesh has UV coordinates defined export them
        has_uv = (hasattr(mesh.visual, 'uv') and
                  mesh.visual.uv is not None and
                  len(mesh.visual.uv) == len(mesh.vertices))
        if has_uv:
            # slice off W if passed
            uv = mesh.visual.uv.copy()[:, :2]
            # reverse the Y for GLTF
            #uv[:, 1] = 1.0 - uv[:, 1]
            # add an accessor describing the blob of UV's
            acc_uv = _data_append(acc=tree['accessors'],
                                  buff=buffer_items,
                                  blob={"componentType": 5126,
                                        "type": "VEC2",
                                        "byteOffset": 0},
                                  data=uv.astype(float32))
            # add the reference for UV coordinates
            current["primitives"][0]["attributes"]["TEXCOORD_0"] = acc_uv
            # only reference the material if we had UV coordinates
            current["primitives"][0]["material"] = current_material
                # if mesh has UV coordinates defined export them
        has_uv1 = (hasattr(mesh.visual, 'vertex_attributes') 
                   and 'uv1' in mesh.visual.vertex_attributes
                   and mesh.visual.vertex_attributes['uv1'] is not None 
                   and len(mesh.visual.vertex_attributes['uv1']) == len(mesh.vertices))
        if has_uv1:
            # slice off W if passed
            uv = mesh.visual.vertex_attributes['uv1'].copy()[:, :2]
            # reverse the Y for GLTF
            #uv[:, 1] = 1.0 - uv[:, 1]
            # add an accessor describing the blob of UV's
            acc_uv = _data_append(acc=tree['accessors'],
                                  buff=buffer_items,
                                  blob={"componentType": 5126,
                                        "type": "VEC2",
                                        "byteOffset": 0},
                                  data=uv.astype(float32))
            # add the reference for UV coordinates
            current["primitives"][0]["attributes"]["TEXCOORD_1"] = acc_uv
        
        has_uv2 = (hasattr(mesh.visual, 'vertex_attributes') 
                   and 'uv2' in mesh.visual.vertex_attributes
                   and mesh.visual.vertex_attributes['uv2'] is not None 
                   and len(mesh.visual.vertex_attributes['uv2']) == len(mesh.vertices))
        if has_uv2:
            # slice off W if passed
            uv = mesh.visual.vertex_attributes['uv2'].copy()[:, :2]
            # reverse the Y for GLTF
            #uv[:, 1] = 1.0 - uv[:, 1]
            # add an accessor describing the blob of UV's
            acc_uv = _data_append(acc=tree['accessors'],
                                  buff=buffer_items,
                                  blob={"componentType": 5126,
                                        "type": "VEC2",
                                        "byteOffset": 0},
                                  data=uv.astype(float32))
            # add the reference for UV coordinates
            current["primitives"][0]["attributes"]["TEXCOORD_2"] = acc_uv

        has_uv3 = (hasattr(mesh.visual, 'vertex_attributes') 
                   and 'uv3' in mesh.visual.vertex_attributes
                   and mesh.visual.vertex_attributes['uv3'] is not None 
                   and len(mesh.visual.vertex_attributes['uv3']) == len(mesh.vertices))
        if has_uv3:
            # slice off W if passed
            uv = mesh.visual.vertex_attributes['uv3'].copy()[:, :2]
            # reverse the Y for GLTF
            #uv[:, 1] = 1.0 - uv[:, 1]
            # add an accessor describing the blob of UV's
            acc_uv = _data_append(acc=tree['accessors'],
                                  buff=buffer_items,
                                  blob={"componentType": 5126,
                                        "type": "VEC2",
                                        "byteOffset": 0},
                                  data=uv.astype(float32))
            # add the reference for UV coordinates
            current["primitives"][0]["attributes"]["TEXCOORD_3"] = acc_uv

    if (include_normals or
        (include_normals is None and
         'vertex_normals' in mesh._cache.cache)):
        # store vertex normals if requested
        if unitize_normals:
            normals = mesh.vertex_normals.copy()
            norms = np.linalg.norm(normals, axis=1)
            if not util.allclose(norms, 1.0, atol=1e-4):
                normals /= norms.reshape((-1, 1))
        else:
            # we don't have to copy them since
            # they aren't being altered
            normals = mesh.vertex_normals

        acc_norm = _data_append(
            acc=tree['accessors'],
            buff=buffer_items,
            blob={"componentType": 5126,
                  "count": len(mesh.vertices),
                  "type": "VEC3",
                  "byteOffset": 0},
            data=normals.astype(float32))
        # add the reference for vertex color
        current["primitives"][0]["attributes"][
            "NORMAL"] = acc_norm

    # for each attribute with a leading underscore, assign them to trimesh
    # vertex_attributes
    for key, attrib in mesh.vertex_attributes.items():
        # Application specific attributes must be
        # prefixed with an underscore
        if not key.startswith("_"):
            key = "_" + key
        # store custom vertex attributes
        current["primitives"][0][
            "attributes"][key] = _data_append(
                acc=tree['accessors'],
                buff=buffer_items,
                blob=_build_accessor(attrib),
                data=attrib)

    tree["meshes"].append(current)