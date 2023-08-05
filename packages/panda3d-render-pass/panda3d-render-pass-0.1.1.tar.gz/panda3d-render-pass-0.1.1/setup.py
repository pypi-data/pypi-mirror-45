# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['panda3d_render_pass']

package_data = \
{'': ['*']}

install_requires = \
['panda3d>=1.10,<2.0']

setup_kwargs = {
    'name': 'panda3d-render-pass',
    'version': '0.1.1',
    'description': 'A Panda3D utility to simplify setting up multi-pass rendering systems',
    'long_description': '# Render Pass\nThis library is intended to make multi-pass rendering a little easier in Panda3D.\nEach RenderPass objects represents a render target and a scene to render.\nIf no scene is given, a fullscreen quad is rendered.\nThis library is meant to replace the FilterManager found in Panda3D\'s Direct library.\n\n## Example\nThe code below was added to the "Roaming Ralph" demo to do HDR rendering.\nThe full sample can be found in `samples/roaming-ralph`.\n```python\n        self.render.set_attrib(LightRampAttrib.make_identity())\n        fb_props = FrameBufferProperties()\n        fb_props.set_float_color(True)\n        fb_props.set_rgba_bits(16, 16, 16, 0)\n        fb_props.set_depth_bits(32)\n\n        scene_pass = RenderPass(\n            \'scene\',\n            camera=base.camera,\n            scene=base.render,\n            frame_buffer_properties=fb_props,\n            clear_color=LColor(0.53, 0.80, 0.92, 1),\n        )\n\n        filter_pass = RenderPass(\n            \'filter\',\n            shader=Shader.load(Shader.SL_GLSL, \'shaders/fsq.vert\', \'shaders/fsq.frag\')\n        )\n        filter_pass._root.set_shader_input(\'render\', scene_pass.output)\n\n        card = filter_pass.buffer.getTextureCard()\n        card.setTexture(filter_pass.output)\n        card.reparentTo(render2d)\n```\n',
    'author': 'Daniel Stokes',
    'author_email': 'kupomail@gmail.com',
    'url': 'https://github.com/Kupoman/panda3d-render-pass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
