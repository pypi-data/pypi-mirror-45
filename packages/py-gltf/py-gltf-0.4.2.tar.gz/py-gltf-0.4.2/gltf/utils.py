import os
import copy
import base64

from PIL import Image as PImage


def binary_to_uri(b, mime_type='application/octet-stream'):
    return 'data:{};base64,{}'.format(mime_type, base64.b64encode(b).decode('utf-8'))


def load_uri(s, folder=None):
    if s.startswith('data:'):
        return base64.b64decode(s[s.index(',') + 1:])

    if folder:
        s = os.path.join(folder, s)
    with open(s, 'rb') as f:
        return f.read()


class BaseGLTFStructure(object):
    name = None

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        # self_data = self.__dict__.copy()
        # self_data.pop('name', None)
        # other_data = other.__dict__.copy()
        # other_data.pop('name', None)
        # return self_data == other_data
        return self.__dict__ == other.__dict__

    # def __hash__(self):
    #     self_data = self.__dict__.copy()
    #     self_data.pop('name', None)
    #     return hash(frozenset(self_data.items()))


def get_version():
    from . import VERSION
    return VERSION


def sample_textures_to_materials(gltf, min_x=0.83, min_y=0.95):
    from .materials import Sampler, Material
    images = dict()
    colors = dict()

    for n in (n for n in gltf.nodes if n.mesh):
    # for n in (n for n in gltf.nodes if n.mesh and n.name in ('m6014_rim_wide_w_hole_11_1',)):
        for p in n.mesh.primitives:
            if p.material is None or not p.texcoords:
                continue

            texcoord_idx = 0 if p.material.color_uv is None else p.material.color_uv
            texcoords = p.texcoords[texcoord_idx]
            indices = p.indices.data if p.indices else list(range(texcoords.count))

            tex = p.material.color_texture or p.material.diffuse_texture
            if tex is None:
                continue
            sampler = tex.sampler or Sampler()
            if id(tex) not in images:
                images[id(tex)] = PImage.open(tex.source.get_fp())
            img = images[id(tex)]

            color = None
            for i in indices:
                point = texcoords.data[i]
                if point[0] < min_x and point[1] < min_y:
                    print(point)
                    break
                # Get the RGBA value for each point
                point = sampler.wrap_point(point)
                x = round((img.size[0] - 1) * point[0])
                y = round((img.size[1] - 1) * point[1])
                pixel = img.getpixel((x, y))
                if len(pixel) < 4:
                    pixel = list(pixel)
                    if len(pixel) == 1:
                        pixel *= 3
                    if len(pixel) == 3:
                        pixel.append(255)
                    else:
                        raise ValueError('Incorrect number of channels in pixel')

                pixel = tuple(pixel)
                if color is None:
                    print(pixel)
                    color = pixel
                if pixel != color:
                    print(pixel)
                    break
            else:
                # All texcoords mapped to the same color
                if color not in colors:
                    new_mat = copy.copy(p.material)
                    new_mat.base_color_factor = [(c/255) ** 2.2 for c in color]
                    new_mat.color_texture = None
                    new_mat.color_uv = None
                    new_mat.name = 'SampledTexture'
                    colors[color] = new_mat
                mat = colors[color]
                p.material = mat

                if texcoord_idx != 0 or len(p.texcoords) > 1:
                    p.texcoords = []
                    continue
                    raise NotImplementedError
                del p.texcoords[texcoord_idx]

    gltf.repair()
