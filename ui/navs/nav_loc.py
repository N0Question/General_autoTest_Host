import configparser
import os
import re
import struct

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtSvg, QtWidgets, uic

try:
    import pyqtgraph.opengl as gl
    _GL_IMPORT_ERROR = None
except Exception as exc:
    gl = None
    _GL_IMPORT_ERROR = exc


class IMUColumnConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, defaults=None, title_list=None):
        super().__init__(parent)
        self._defaults = defaults or {}
        self._title_list = title_list or []
        self._build_ui()

    def _build_ui(self):
        ui_path = os.path.join(os.path.dirname(__file__), 'IMUColumnConfigDialog.ui')
        uic.loadUi(ui_path, self)
        self._apply_defaults()
        self._refresh_preview()

        for editor in [
            self.edit_lon_col,
            self.edit_lat_col,
            self.edit_east_col,
            self.edit_north_col,
            self.edit_up_col,
            self.edit_stand_east,
            self.edit_stand_north,
            self.edit_stand_up,
            self.edit_pitch_col,
            self.edit_roll_col,
            self.edit_yaw_col,
        ]:
            editor.textChanged.connect(self._refresh_preview)

    def _apply_defaults(self):
        default_map = {
            'edit_target_tab': self._defaults.get('target_tab', 1),
            'edit_stand_tab': self._defaults.get('stand_tab', 1),
            'edit_lon_col': self._defaults.get('lon_col', '1'),
            'edit_lat_col': self._defaults.get('lat_col', '1'),
            'edit_east_col': self._defaults.get('east_col', '1'),
            'edit_north_col': self._defaults.get('north_col', '1'),
            'edit_up_col': self._defaults.get('up_col', '1'),
            'edit_stand_lon': self._defaults.get('stand_lon', '116.50271'),
            'edit_stand_lat': self._defaults.get('stand_lat', '39.73155'),
            'edit_radar_range': self._defaults.get('radar_range', '500 1000 1500'),
            'edit_stand_east': self._defaults.get('stand_east_col', ''),
            'edit_stand_north': self._defaults.get('stand_north_col', ''),
            'edit_stand_up': self._defaults.get('stand_up_col', ''),
            'edit_pitch_col': self._defaults.get('pitch_col', '1'),
            'edit_roll_col': self._defaults.get('roll_col', '1'),
            'edit_yaw_col': self._defaults.get('yaw_col', '1'),
            'edit_skip': self._defaults.get('skip_count', '1'),
            'edit_end': self._defaults.get('end_count', '0'),
            'edit_roll': self._defaults.get('rolling', '1'),
        }
        for object_name, default_value in default_map.items():
            editor = getattr(self, object_name, None)
            if editor is not None:
                editor.setText(str(default_value))

    def _parse_axis(self, text_value):
        if text_value is None:
            return None
        text_value = str(text_value).strip()
        if len(text_value) == 0:
            return None
        try:
            return int(text_value.split()[0])
        except Exception:
            return None

    def _title_of_axis(self, axis):
        if axis is None:
            return '未解析'
        if axis < 0 or axis >= len(self._title_list):
            return '越界'
        return self._title_list[axis]

    def _refresh_preview(self):
        preview_lines = []
        preview_items = [
            ('经度', self.edit_lon_col.text()),
            ('纬度', self.edit_lat_col.text()),
            ('东速', self.edit_east_col.text()),
            ('北速', self.edit_north_col.text()),
            ('天速', self.edit_up_col.text()),
            ('基准东速', self.edit_stand_east.text()),
            ('基准北速', self.edit_stand_north.text()),
            ('基准天速', self.edit_stand_up.text()),
            ('俯仰', self.edit_pitch_col.text()),
            ('滚转', self.edit_roll_col.text()),
            ('航向', self.edit_yaw_col.text()),
        ]
        for display_name, axis_text in preview_items:
            axis_index = self._parse_axis(axis_text)
            preview_lines.append('{}: {} -> {}'.format(display_name, axis_text, self._title_of_axis(axis_index)))
        self.preview.setText('\n'.join(preview_lines))

    def get_config(self):
        return {
            'target_tab': self.edit_target_tab.text().strip(),
            'stand_tab': self.edit_stand_tab.text().strip(),
            'lon_col': self.edit_lon_col.text().strip(),
            'lat_col': self.edit_lat_col.text().strip(),
            'east_col': self.edit_east_col.text().strip(),
            'north_col': self.edit_north_col.text().strip(),
            'up_col': self.edit_up_col.text().strip(),
            'stand_lon': self.edit_stand_lon.text().strip(),
            'stand_lat': self.edit_stand_lat.text().strip(),
            'radar_range': self.edit_radar_range.text().strip(),
            'stand_east_col': self.edit_stand_east.text().strip(),
            'stand_north_col': self.edit_stand_north.text().strip(),
            'stand_up_col': self.edit_stand_up.text().strip(),
            'pitch_col': self.edit_pitch_col.text().strip(),
            'roll_col': self.edit_roll_col.text().strip(),
            'yaw_col': self.edit_yaw_col.text().strip(),
            'skip_count': self.edit_skip.text().strip(),
            'end_count': self.edit_end.text().strip(),
            'rolling': self.edit_roll.text().strip(),
        }


class MainWindowNavLoc:
    def __init__(self, mainWindow):
        self.mw = mainWindow
        self.radar_adp = None
        self._radar_circle_items = []
        self._radar_ref_item = None
        self._map_item = None
        self._map_enabled = False
        self._map_auto_fit = True
        self._map_bounds = None
        self._map_config_path = self._resolve_workspace_path('./配置文件/map_config.ini')
        self._attitude_plot_adp = None
        self._attitude_wire_item = None
        self._attitude_label_item = None
        self._attitude_gl_widget = None
        self._attitude_mesh_item = None
        self._attitude_axis_item = None
        self._attitude_axis_lines = []
        self._attitude_axis_text_items = []
        self._attitude_grid_item = None
        self._attitude_grid_lines = []
        self._attitude_vertices = None
        self._attitude_faces = None
        self._attitude_edges = None
        self._attitude_has_stl = False
        self._attitude_use_gl = False
        self._attitude_status = ''
        self._attitude_last = {'pitch': 0.0, 'roll': 0.0, 'yaw': 0.0}
        
        self.init_inu_plot_items_lazy()
        self.load_map_config()
        map_loaded = self.load_offline_map()
        self.init_radar(fit_view=not map_loaded)
        self.init_logic()

    def _resolve_workspace_path(self, path_text):
        normalized_path = os.path.normpath(path_text)
        if os.path.isabs(normalized_path):
            return normalized_path
        return os.path.normpath(os.path.join(os.getcwd(), normalized_path))

    def _append_nav_message(self, message_text):
        if hasattr(self.mw, 'list_init_msg') and isinstance(self.mw.list_init_msg, list):
            self.mw.list_init_msg.append(message_text)

    def _get_map_default_config(self):
        return {
            'enabled': False,
            'mode': 'xyz_tiles',
            'path': './地图资源/底图/beijing_location_map_2_cc0.svg',
            'tile_dir': './地图资源/瓦片/beijing_osm_z19_demo',
            'tile_zoom': 19,
            'tile_x_min': 431533,
            'tile_x_max': 431541,
            'tile_y_min': 198989,
            'tile_y_max': 198997,
            'tile_ext': 'png',
            'min_lon': 116.20,
            'max_lon': 116.70,
            'min_lat': 39.70,
            'max_lat': 40.10,
            'opacity': 0.90,
            'auto_fit': True,
            'lock_aspect': True,
            'rotation_degrees': 0,
            'tile_rotation_degrees': 90,
            'flip_vertical': True,
            'flip_horizontal': False,
            'tile_flip_vertical': False,
            'tile_flip_horizontal': False,
            'tile_offset_east_m': 0.0,
            'tile_offset_north_m': 0.0,
            'svg_render_width': 8192,
            'svg_render_height': 0,
        }

    def _read_map_config(self):
        map_config = self._get_map_default_config()
        if not os.path.exists(self._map_config_path):
            self._append_nav_message('离线地图配置不存在，已跳过: {}'.format(self._map_config_path))
            return map_config

        parser = configparser.ConfigParser()
        last_error = None
        for encoding_name in ['gb2312', 'gbk', 'utf-8', 'utf-8-sig']:
            try:
                with open(self._map_config_path, 'r', encoding=encoding_name, errors='strict') as config_file:
                    parser.read_file(config_file)
                last_error = None
                break
            except Exception as exc:
                parser = configparser.ConfigParser()
                last_error = exc
        if last_error is not None:
            self._append_nav_message('离线地图配置读取失败: {}'.format(last_error))
            return map_config

        if not parser.has_section('offline_map'):
            self._append_nav_message('离线地图配置缺少 [offline_map] 段，已使用默认值')
            return map_config

        config_section = parser['offline_map']
        try:
            map_config['enabled'] = config_section.getboolean('enabled', fallback=map_config['enabled'])
        except ValueError:
            pass
        map_config['mode'] = config_section.get('mode', fallback=map_config['mode']).strip().lower()
        map_config['path'] = config_section.get('path', fallback=map_config['path'])
        map_config['tile_dir'] = config_section.get('tile_dir', fallback=map_config['tile_dir'])
        map_config['tile_ext'] = config_section.get('tile_ext', fallback=map_config['tile_ext'])
        for key_name in ['min_lon', 'max_lon', 'min_lat', 'max_lat', 'opacity', 'tile_offset_east_m', 'tile_offset_north_m']:
            try:
                map_config[key_name] = float(config_section.get(key_name, fallback=map_config[key_name]))
            except (TypeError, ValueError):
                pass
        for key_name in ['svg_render_width', 'svg_render_height', 'tile_zoom', 'tile_x_min', 'tile_x_max', 'tile_y_min', 'tile_y_max', 'rotation_degrees', 'tile_rotation_degrees']:
            try:
                map_config[key_name] = int(config_section.get(key_name, fallback=map_config[key_name]))
            except (TypeError, ValueError):
                pass
        for key_name in ['auto_fit', 'lock_aspect', 'flip_vertical', 'flip_horizontal', 'tile_flip_vertical', 'tile_flip_horizontal']:
            try:
                map_config[key_name] = config_section.getboolean(key_name, fallback=map_config[key_name])
            except ValueError:
                pass
        return map_config

    def load_map_config(self):
        self._map_config = self._read_map_config()
        self._map_enabled = bool(self._map_config.get('enabled', False))
        self._map_auto_fit = bool(self._map_config.get('auto_fit', True))
        self._map_bounds = {
            'min_lon': float(self._map_config['min_lon']),
            'max_lon': float(self._map_config['max_lon']),
            'min_lat': float(self._map_config['min_lat']),
            'max_lat': float(self._map_config['max_lat']),
        }
        self.graphicsView_INU_loc_adp.setAspectLocked(bool(self._map_config.get('lock_aspect', True)))

    def _tile_xyz_to_lon_lat(self, tile_x, tile_y, zoom_level):
        scale = float(1 << int(zoom_level))
        lon = float(tile_x) / scale * 360.0 - 180.0
        lat_rad = np.arctan(np.sinh(np.pi * (1.0 - 2.0 * float(tile_y) / scale)))
        lat = float(np.degrees(lat_rad))
        return lon, lat

    def _offset_bounds_by_meters(self, bounds, east_m=0.0, north_m=0.0):
        east_m = float(east_m)
        north_m = float(north_m)
        if abs(east_m) < 1e-9 and abs(north_m) < 1e-9:
            return dict(bounds)

        center_lat = (float(bounds['min_lat']) + float(bounds['max_lat'])) / 2.0
        meter_per_deg_lat = np.pi * 6378137.0 / 180.0
        meter_per_deg_lon = meter_per_deg_lat * max(np.cos(np.deg2rad(center_lat)), 1e-6)
        lon_offset = east_m / meter_per_deg_lon
        lat_offset = north_m / meter_per_deg_lat
        return {
            'min_lon': float(bounds['min_lon']) + lon_offset,
            'max_lon': float(bounds['max_lon']) + lon_offset,
            'min_lat': float(bounds['min_lat']) + lat_offset,
            'max_lat': float(bounds['max_lat']) + lat_offset,
        }

    def _clear_map_item(self):
        if self._map_item is None:
            return
        try:
            self.graphicsView_INU_loc_adp.removeItem(self._map_item)
        except Exception:
            pass
        self._map_item = None

    def _qimage_to_rgba_array(self, image, flip_vertical=False, flip_horizontal=False, rotation_degrees=0):
        converted_image = image.convertToFormat(QtGui.QImage.Format_RGBA8888)
        width = converted_image.width()
        height = converted_image.height()
        ptr = converted_image.bits()
        ptr.setsize(converted_image.byteCount())
        rgba_array = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, 4)).copy()
        normalized_rotation = int(rotation_degrees) % 360
        if normalized_rotation == 90:
            rgba_array = np.rot90(rgba_array, k=3)
        elif normalized_rotation == 180:
            rgba_array = np.rot90(rgba_array, k=2)
        elif normalized_rotation == 270:
            rgba_array = np.rot90(rgba_array, k=1)
        if flip_vertical:
            rgba_array = np.flipud(rgba_array)
        if flip_horizontal:
            rgba_array = np.fliplr(rgba_array)
        return rgba_array

    def _find_existing_tile_path(self, tile_dir, zoom_level, tile_x, tile_y, configured_ext):
        ext_candidates = []
        normalized_ext = str(configured_ext or '').strip().lower().lstrip('.')
        if normalized_ext:
            ext_candidates.append(normalized_ext)
        for ext_name in ['png', 'jpg', 'jpeg', 'webp', 'bmp']:
            if ext_name not in ext_candidates:
                ext_candidates.append(ext_name)

        for ext_name in ext_candidates:
            candidate_path = os.path.join(tile_dir, str(zoom_level), str(tile_x), '{}.{}'.format(tile_y, ext_name))
            if os.path.exists(candidate_path):
                return candidate_path
        return None

    def _infer_xyz_tile_layout(self, tile_dir, configured_zoom=None, configured_ext='png'):
        if not os.path.isdir(tile_dir):
            return None

        zoom_candidates = []
        for child_name in os.listdir(tile_dir):
            child_path = os.path.join(tile_dir, child_name)
            if os.path.isdir(child_path) and child_name.isdigit():
                zoom_candidates.append(int(child_name))

        if not zoom_candidates:
            return None

        zoom_level = None
        if configured_zoom is not None and int(configured_zoom) in zoom_candidates:
            zoom_level = int(configured_zoom)
        elif len(zoom_candidates) == 1:
            zoom_level = zoom_candidates[0]
        else:
            zoom_level = min(zoom_candidates)

        zoom_dir = os.path.join(tile_dir, str(zoom_level))
        tile_x_values = []
        tile_y_values = []
        discovered_ext = ''
        normalized_ext = str(configured_ext or '').strip().lower().lstrip('.')

        for x_name in os.listdir(zoom_dir):
            x_dir = os.path.join(zoom_dir, x_name)
            if not os.path.isdir(x_dir) or not x_name.isdigit():
                continue
            y_found = False
            for tile_name in os.listdir(x_dir):
                tile_path = os.path.join(x_dir, tile_name)
                if not os.path.isfile(tile_path):
                    continue
                tile_stem, tile_ext = os.path.splitext(tile_name)
                if not tile_stem.isdigit():
                    continue
                tile_ext = tile_ext.lower().lstrip('.')
                if normalized_ext and tile_ext != normalized_ext:
                    continue
                tile_x_values.append(int(x_name))
                tile_y_values.append(int(tile_stem))
                if not discovered_ext:
                    discovered_ext = tile_ext
                y_found = True
            if not y_found and not normalized_ext:
                continue

        if not tile_x_values or not tile_y_values:
            if normalized_ext:
                return self._infer_xyz_tile_layout(tile_dir, configured_zoom=zoom_level, configured_ext='')
            return None

        return {
            'zoom_level': zoom_level,
            'tile_x_min': min(tile_x_values),
            'tile_x_max': max(tile_x_values),
            'tile_y_min': min(tile_y_values),
            'tile_y_max': max(tile_y_values),
            'tile_ext': discovered_ext or normalized_ext or 'png',
        }

    def _load_xyz_tile_mosaic(self):
        tile_dir = self._resolve_workspace_path(self._map_config.get('tile_dir', ''))
        if not os.path.isdir(tile_dir):
            self._append_nav_message('离线瓦片目录不存在: {}'.format(tile_dir))
            return QtGui.QImage(), None, ''

        configured_ext = self._map_config.get('tile_ext', 'png')
        inferred_layout = self._infer_xyz_tile_layout(
            tile_dir,
            configured_zoom=self._map_config.get('tile_zoom', 19),
            configured_ext=configured_ext,
        )
        if inferred_layout is None:
            self._append_nav_message('离线瓦片目录中未识别到有效的 z/x/y 结构: {}'.format(tile_dir))
            return QtGui.QImage(), None, ''

        zoom_level = int(inferred_layout['zoom_level'])
        tile_x_min = int(inferred_layout['tile_x_min'])
        tile_x_max = int(inferred_layout['tile_x_max'])
        tile_y_min = int(inferred_layout['tile_y_min'])
        tile_y_max = int(inferred_layout['tile_y_max'])
        configured_ext = inferred_layout['tile_ext']
        if tile_x_min > tile_x_max or tile_y_min > tile_y_max:
            self._append_nav_message('离线瓦片范围无效，请检查 tile_x/tile_y 配置')
            return QtGui.QImage(), None, ''

        tile_columns = tile_x_max - tile_x_min + 1
        tile_rows = tile_y_max - tile_y_min + 1
        first_tile_image = None
        first_tile_size = None
        found_tile_count = 0

        for tile_y in range(tile_y_min, tile_y_max + 1):
            for tile_x in range(tile_x_min, tile_x_max + 1):
                tile_path = self._find_existing_tile_path(tile_dir, zoom_level, tile_x, tile_y, configured_ext)
                if not tile_path:
                    continue
                tile_image = QtGui.QImage(tile_path)
                if tile_image.isNull():
                    continue
                first_tile_image = tile_image
                first_tile_size = tile_image.size()
                break
            if first_tile_image is not None:
                break

        if first_tile_image is None or first_tile_size is None:
            self._append_nav_message('离线瓦片目录中未找到可用图片: {}'.format(tile_dir))
            return QtGui.QImage(), None, ''

        mosaic_image = QtGui.QImage(
            first_tile_size.width() * tile_columns,
            first_tile_size.height() * tile_rows,
            QtGui.QImage.Format_RGBA8888,
        )
        mosaic_image.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(mosaic_image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, False)

        for row_index, tile_y in enumerate(range(tile_y_min, tile_y_max + 1)):
            for col_index, tile_x in enumerate(range(tile_x_min, tile_x_max + 1)):
                tile_path = self._find_existing_tile_path(tile_dir, zoom_level, tile_x, tile_y, configured_ext)
                if not tile_path:
                    continue
                tile_image = QtGui.QImage(tile_path)
                if tile_image.isNull():
                    continue
                if tile_image.size() != first_tile_size:
                    tile_image = tile_image.scaled(first_tile_size, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
                painter.drawImage(col_index * first_tile_size.width(), row_index * first_tile_size.height(), tile_image)
                found_tile_count += 1
        painter.end()

        min_lon, max_lat = self._tile_xyz_to_lon_lat(tile_x_min, tile_y_min, zoom_level)
        max_lon, min_lat = self._tile_xyz_to_lon_lat(tile_x_max + 1, tile_y_max + 1, zoom_level)
        bounds = {
            'min_lon': min_lon,
            'max_lon': max_lon,
            'min_lat': min_lat,
            'max_lat': max_lat,
        }
        bounds = self._offset_bounds_by_meters(
            bounds,
            east_m=self._map_config.get('tile_offset_east_m', 0.0),
            north_m=self._map_config.get('tile_offset_north_m', 0.0),
        )
        title_text = '离线瓦片: z{} x{}-{} y{}-{} ({} tiles)'.format(
            zoom_level,
            tile_x_min,
            tile_x_max,
            tile_y_min,
            tile_y_max,
            found_tile_count,
        )
        return mosaic_image, bounds, title_text

    def _render_svg_image(self, image_path):
        svg_renderer = QtSvg.QSvgRenderer(image_path)
        if not svg_renderer.isValid():
            return QtGui.QImage()

        default_size = svg_renderer.defaultSize()
        if not default_size.isValid() or default_size.width() <= 0 or default_size.height() <= 0:
            default_size = QtCore.QSize(422, 338)

        render_width = max(512, int(self._map_config.get('svg_render_width', default_size.width())))
        render_width = min(render_width, 8192)
        render_height = int(self._map_config.get('svg_render_height', 0))
        if render_height <= 0:
            aspect_ratio = default_size.height() / max(default_size.width(), 1)
            render_height = max(512, int(round(render_width * aspect_ratio)))
        render_height = min(render_height, 8192)

        image = QtGui.QImage(render_width, render_height, QtGui.QImage.Format_RGBA8888)
        image.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        svg_renderer.render(painter, QtCore.QRectF(0, 0, render_width, render_height))
        painter.end()
        return image

    def load_offline_map(self):
        self._clear_map_item()
        if not getattr(self, '_map_config', None):
            self.load_map_config()
        if not self._map_enabled:
            self._append_nav_message('离线地图未启用，导航页使用网格视图')
            return False

        map_mode = str(self._map_config.get('mode', 'image')).strip().lower()
        title_text = ''
        bounds = dict(self._map_bounds or {})

        if map_mode == 'xyz_tiles':
            image, bounds, title_text = self._load_xyz_tile_mosaic()
        else:
            image_path = self._resolve_workspace_path(self._map_config.get('path', ''))
            if not os.path.exists(image_path):
                self._append_nav_message('离线地图文件不存在，已回退为纯轨迹视图: {}'.format(image_path))
                return False

            if os.path.splitext(image_path)[1].lower() == '.svg':
                image = self._render_svg_image(image_path)
                render_width = int(self._map_config.get('svg_render_width', image.width()))
                title_text = '离线地图: {} (SVG {})'.format(os.path.basename(image_path), render_width)
            else:
                image_reader = QtGui.QImageReader(image_path)
                image_reader.setAutoTransform(True)
                image = image_reader.read()
                title_text = '离线地图: {}'.format(os.path.basename(image_path))
        if image.isNull():
            if map_mode == 'xyz_tiles':
                self._append_nav_message('离线瓦片拼接失败，已回退为纯轨迹视图')
            elif os.path.splitext(image_path)[1].lower() == '.svg':
                self._append_nav_message('离线 SVG 地图读取失败: {}'.format(image_path))
            else:
                self._append_nav_message('离线地图读取失败: {}'.format(image_reader.errorString()))
            return False

        if map_mode == 'xyz_tiles':
            map_array = self._qimage_to_rgba_array(
                image,
                flip_vertical=bool(self._map_config.get('tile_flip_vertical', False)),
                flip_horizontal=bool(self._map_config.get('tile_flip_horizontal', False)),
                rotation_degrees=int(self._map_config.get('tile_rotation_degrees', 0)),
            )
        else:
            map_array = self._qimage_to_rgba_array(
                image,
                flip_vertical=bool(self._map_config.get('flip_vertical', True)),
                flip_horizontal=bool(self._map_config.get('flip_horizontal', False)),
                rotation_degrees=int(self._map_config.get('rotation_degrees', 0)),
            )
        map_item = pg.ImageItem(map_array)
        map_item.setOpacity(max(0.0, min(float(self._map_config.get('opacity', 0.9)), 1.0)))
        map_item.setZValue(-100)

        min_lon = float(bounds['min_lon'])
        max_lon = float(bounds['max_lon'])
        min_lat = float(bounds['min_lat'])
        max_lat = float(bounds['max_lat'])
        if min_lon >= max_lon or min_lat >= max_lat:
            self._append_nav_message('离线地图经纬度边界无效，已回退为纯轨迹视图')
            return False

        map_item.setRect(QtCore.QRectF(min_lon, min_lat, max_lon - min_lon, max_lat - min_lat))
        self.graphicsView_INU_loc_adp.addItem(map_item)
        self._map_item = map_item
        self._map_bounds = bounds
        self.graphicsView_INU_loc_adp.setTitle(title_text or '离线地图')

        if self._map_auto_fit:
            self.fit_navigation_view(prefer_map=True)
        return True

    def fit_navigation_view(self, prefer_map=False):
        if prefer_map and self._map_item is not None and self._map_bounds:
            min_lon = self._map_bounds['min_lon']
            max_lon = self._map_bounds['max_lon']
            min_lat = self._map_bounds['min_lat']
            max_lat = self._map_bounds['max_lat']
            self.graphicsView_INU_loc_adp.setXRange(min_lon, max_lon, padding=0.02)
            self.graphicsView_INU_loc_adp.setYRange(min_lat, max_lat, padding=0.02)
            return

        if self._radar_circle_items:
            x_list = []
            y_list = []
            for curve_item in self._radar_circle_items:
                x_values, y_values = curve_item.getData()
                if x_values is None or y_values is None:
                    continue
                if len(x_values) == 0 or len(y_values) == 0:
                    continue
                x_list.append(np.asarray(x_values))
                y_list.append(np.asarray(y_values))
            if x_list and y_list:
                x_all = np.concatenate(x_list)
                y_all = np.concatenate(y_list)
                self.graphicsView_INU_loc_adp.setXRange(float(np.nanmin(x_all)), float(np.nanmax(x_all)), padding=0.15)
                self.graphicsView_INU_loc_adp.setYRange(float(np.nanmin(y_all)), float(np.nanmax(y_all)), padding=0.15)

    def reload_navigation_view(self):
        self.load_map_config()
        map_loaded = self.load_offline_map()
        self.init_radar(fit_view=not map_loaded)
        
    # 懒加载初始化INU绘图项
    def init_inu_plot_items_lazy(self):
        config_background_color = self.mw.init_ini.config_background_color
        config_main_line_color = self.mw.init_ini.config_main_line_color
        config_line_width = self.mw.init_ini.config_line_width
        # 轨迹相关配置
        config_trace_color = self.mw.init_ini.config_trace_color
        config_trace_point_size = self.mw.init_ini.config_trace_point_size
        config_trace_point_alpha = self.mw.init_ini.config_trace_point_alpha
        config_trace_end_color = self.mw.init_ini.config_trace_end_color
        config_trace_start_color = self.mw.init_ini.config_trace_start_color
        config_trace_endpoint_size = self.mw.init_ini.config_trace_endpoint_size
        
        for graphicsView in [self.mw.graphicsView_INU_loc, self.mw.graphicsView_INU_loc_error, self.mw.graphicsView_INU_speed, self.mw.graphicsView_INU_attitude]:
            graphicsView.setBackground(config_background_color)

        self.graphicsView_INU_loc_adp = self.mw.graphicsView_INU_loc.addPlot()
        self.graphicsView_INU_loc_error_adp = self.mw.graphicsView_INU_loc_error.addPlot()
        self.graphicsView_INU_speed_adp = self.mw.graphicsView_INU_speed.addPlot()
        self.graphicsView_INU_loc_adp.showGrid(x=True, y=True, alpha=1.0)
        self.graphicsView_INU_loc_adp.setAspectLocked(True)
        self.graphicsView_INU_loc_adp.getViewBox().setMouseEnabled(x=True, y=True)
        self.graphicsView_INU_loc_adp.getViewBox().setMouseMode(pg.ViewBox.PanMode)
        self.graphicsView_INU_loc_error_adp.showGrid(x=True, y=True, alpha=self.mw.default_alpha)
        self.graphicsView_INU_speed_adp.showGrid(x=True, y=True, alpha=self.mw.default_alpha)

        # 从HEX颜色转换为RGB
        trace_rgb = self._hex_to_rgb(config_trace_color)
        end_color = self._hex_to_rgb(config_trace_end_color)
        start_color = self._hex_to_rgb(config_trace_start_color)
        
        # 创建轨迹点散点图，使用配置的颜色、大小和透明度
        self.mw.scatter = pg.ScatterPlotItem(
            size=config_trace_point_size, 
            pen=None, 
            brush=pg.mkBrush(trace_rgb[0], trace_rgb[1], trace_rgb[2], config_trace_point_alpha)
        )
        self.mw.scatter.setZValue(20)
        self.graphicsView_INU_loc_adp.addItem(self.mw.scatter)
        # self.mw.scatter.setData([1, 2, 3], [5, 6, 7])
        
        # 创建轨迹终点散点图
        self.mw.scatterEnd = pg.ScatterPlotItem(size=config_trace_endpoint_size, brush=end_color)
        self.mw.scatterEnd.setZValue(30)
        self.graphicsView_INU_loc_adp.addItem(self.mw.scatterEnd)
        
        # 创建轨迹起点散点图
        self.mw.scatterBegin = pg.ScatterPlotItem(size=config_trace_endpoint_size, brush=start_color)
        self.mw.scatterBegin.setZValue(30)
        self.graphicsView_INU_loc_adp.addItem(self.mw.scatterBegin)
        
        self.mw.gv_pen_loc_error = self.graphicsView_INU_loc_error_adp.plot(
            pen=pg.mkPen(color=config_main_line_color, width=config_line_width)
        )
        self.mw.gv_pen_speed = self.graphicsView_INU_speed_adp.plot(
            pen=pg.mkPen(color=config_main_line_color, width=config_line_width)
        )
        self._init_attitude_view(
            background_color=config_background_color,
            line_width=config_line_width,
        )
        self._init_attitude_mesh()
        # 初始先绘制一帧零姿态，避免仅显示状态文字。
        self.update_attitude_plot(0.0, 0.0, 0.0)
        self.radar_adp = self.graphicsView_INU_loc_adp

    def _hex_to_rgb(self, color_value):
        """将HEX颜色值转换为RGB元组(R, G, B)"""
        color_str = str(color_value).strip()
        if len(color_str) == 0:
            return (255, 0, 0)  # 默认红色
        if not color_str.startswith('#'):
            color_str = '#{}'.format(color_str)
        color_str = color_str.lstrip('#')
        try:
            if len(color_str) == 6:
                r = int(color_str[0:2], 16)
                g = int(color_str[2:4], 16)
                b = int(color_str[4:6], 16)
                return (r, g, b)
        except Exception:
            pass
        return (255, 0, 0)  # 默认红色

    def _hex_to_qcolor(self, color_value):
        color_str = str(color_value).strip()
        if len(color_str) == 0:
            return QtGui.QColor(20, 20, 20)
        if not color_str.startswith('#'):
            color_str = '#{}'.format(color_str)
        color = QtGui.QColor(color_str)
        if not color.isValid():
            return QtGui.QColor(20, 20, 20)
        return color

    def _init_attitude_view(self, background_color, line_width):
        self._attitude_use_gl = False
        if gl is None and _GL_IMPORT_ERROR is not None:
            self._append_nav_message('姿态3D依赖缺失: {}'.format(_GL_IMPORT_ERROR))
        if gl is not None:
            try:
                container = self.mw.graphicsView_INU_attitude.parentWidget()
                layout = container.layout() if container is not None else None

                new_gl_widget = gl.GLViewWidget(container)
                new_gl_widget.setMinimumSize(0, 0)
                new_gl_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

                bg_color = self._hex_to_qcolor(background_color)
                new_gl_widget.setBackgroundColor(bg_color)
                new_gl_widget.setCameraPosition(distance=4.2, elevation=18, azimuth=42)
                new_gl_widget.setFocusPolicy(QtCore.Qt.StrongFocus)

                # 3D控件初始化成功后再替换，避免异常时原控件被隐藏造成空白。
                if layout is not None:
                    layout.removeWidget(self.mw.graphicsView_INU_attitude)
                self.mw.graphicsView_INU_attitude.hide()

                self._attitude_gl_widget = new_gl_widget
                if layout is not None:
                    layout.addWidget(self._attitude_gl_widget)

                self._init_black_gl_grid(grid_size=3.0, grid_spacing=0.25, z_shift=0.0)

                self._attitude_axis_item = gl.GLAxisItem()
                self._attitude_axis_item.setSize(x=1.2, y=1.2, z=1.2)
                self._attitude_gl_widget.addItem(self._attitude_axis_item)

                self._attitude_use_gl = True
                self._init_attitude_axis_overlay(max(2.0, float(line_width) * 2.2))

                # 修复拉伸窗口时姿态区高度不变：强制姿态容器参与垂直方向伸缩。
                if hasattr(self.mw, 'groupBox_21'):
                    self.mw.groupBox_21.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                    self.mw.groupBox_21.setMinimumHeight(0)
                if hasattr(self.mw, 'verticalLayout_14'):
                    self.mw.verticalLayout_14.setStretch(0, 1)
                    self.mw.verticalLayout_14.setStretch(1, 1)
                    self.mw.verticalLayout_14.setStretch(2, 1)

                self._append_nav_message('姿态视图启用3D模式: 支持鼠标拖拽旋转/滚轮缩放')
                return
            except Exception as exc:
                self._append_nav_message('姿态3D视图初始化失败，回退2D: {}'.format(exc))

        # 回退到2D线框显示
        self.mw.graphicsView_INU_attitude.show()
        self._attitude_plot_adp = self.mw.graphicsView_INU_attitude.addPlot()
        self._attitude_plot_adp.showGrid(x=False, y=False)
        self._attitude_plot_adp.hideAxis('left')
        self._attitude_plot_adp.hideAxis('bottom')
        self._attitude_plot_adp.setAspectLocked(True)
        self._init_black_2d_grid()
        self._attitude_wire_item = self._attitude_plot_adp.plot(
            pen=pg.mkPen(color=(0, 255, 180), width=max(1, int(line_width)))
        )
        self._attitude_label_item = pg.TextItem('', color=(240, 240, 240), anchor=(0, 1))
        self._attitude_plot_adp.addItem(self._attitude_label_item)
        self._attitude_label_item.setPos(-1.35, 1.35)
        self._attitude_plot_adp.setXRange(-1.4, 1.4, padding=0)
        self._attitude_plot_adp.setYRange(-1.4, 1.4, padding=0)

    def _init_black_gl_grid(self, grid_size, grid_spacing, z_shift=0.0):
        if self._attitude_gl_widget is None:
            return

        self._attitude_grid_lines = []
        half = float(grid_size) / 2.0
        spacing = max(float(grid_spacing), 1e-6)
        x_values = np.arange(-half, half + spacing * 0.5, spacing)
        z_values = np.arange(-half, half + spacing * 0.5, spacing)
        grid_color = (0.0, 0.0, 0.0, 1.0)

        # 绘制水平网格: XY平面, Z保持常量。
        for x_val in x_values:
            pos = np.array(
                [[x_val, -half, z_shift], [x_val, half, z_shift]],
                dtype=float,
            )
            line_item = gl.GLLinePlotItem(pos=pos, color=grid_color, width=1.0, antialias=True, mode='lines')
            self._attitude_gl_widget.addItem(line_item)
            self._attitude_grid_lines.append(line_item)

        for y_val in z_values:
            pos = np.array(
                [[-half, y_val, z_shift], [half, y_val, z_shift]],
                dtype=float,
            )
            line_item = gl.GLLinePlotItem(pos=pos, color=grid_color, width=1.0, antialias=True, mode='lines')
            self._attitude_gl_widget.addItem(line_item)
            self._attitude_grid_lines.append(line_item)

    def _init_black_2d_grid(self):
        if self._attitude_plot_adp is None:
            return
        half = 1.35
        spacing = 0.25
        tick_values = np.arange(-half, half + spacing * 0.5, spacing)
        grid_pen = pg.mkPen(color=(0, 0, 0), width=1)
        for x_val in tick_values:
            self._attitude_plot_adp.plot(
                [x_val, x_val],
                [-half, half],
                pen=grid_pen,
            )
        for y_val in tick_values:
            self._attitude_plot_adp.plot(
                [-half, half],
                [y_val, y_val],
                pen=grid_pen,
            )

    def _init_attitude_axis_overlay(self, axis_width):
        if not self._attitude_use_gl or self._attitude_gl_widget is None:
            return

        self._attitude_axis_lines = []
        self._attitude_axis_text_items = []
        # 将坐标轴定义为机体系FRD: X前、Y右、Z下。
        axis_specs = [
            ('X', (1.0, 0.15, 0.15, 0.98), np.array([[0.0, 0.0, 0.0], [0.0, -1.5, 0.0]], dtype=float), (0.0, -1.62, 0.0)),
            ('Y', (0.15, 1.0, 0.15, 0.98), np.array([[0.0, 0.0, 0.0], [-1.5, 0.0, 0.0]], dtype=float), (-1.62, 0.0, 0.0)),
            ('Z', (0.20, 0.45, 1.0, 0.98), np.array([[0.0, 0.0, 0.0], [0.0, 0.0, -1.5]], dtype=float), (0.0, 0.0, -1.62)),
        ]

        for _, color_rgba, positions, _ in axis_specs:
            line_item = gl.GLLinePlotItem(
                pos=positions,
                color=color_rgba,
                width=float(axis_width),
                antialias=True,
                mode='lines',
            )
            self._attitude_gl_widget.addItem(line_item)
            self._attitude_axis_lines.append(line_item)

        if hasattr(gl, 'GLTextItem'):
            for axis_text, color_rgba, _, text_pos in axis_specs:
                text_item = gl.GLTextItem(
                    pos=text_pos,
                    text=axis_text,
                    color=QtGui.QColor(
                        int(color_rgba[0] * 255),
                        int(color_rgba[1] * 255),
                        int(color_rgba[2] * 255),
                    ),
                )
                self._attitude_gl_widget.addItem(text_item)
                self._attitude_axis_text_items.append(text_item)
        else:
            self._append_nav_message('当前pyqtgraph版本不支持GLTextItem，已仅显示彩色坐标轴')

    def _stl_paths(self):
        return [
            self._resolve_workspace_path('./地图资源/aircraft.stl'),
            self._resolve_workspace_path('./aircraft.stl'),
        ]

    def _set_attitude_status(self, status_text):
        self._attitude_status = status_text
        if self._attitude_label_item is not None:
            self._attitude_label_item.setText(status_text)
        if self._attitude_use_gl:
            self._append_nav_message(status_text)

    def _decode_ascii_stl(self, content_bytes):
        text_data = content_bytes.decode('utf-8', errors='ignore')
        vertices = []
        face_indices = []
        vertex_buffer = []
        for line_text in text_data.splitlines():
            line_text = line_text.strip().lower()
            if not line_text.startswith('vertex'):
                continue
            parts = line_text.split()
            if len(parts) != 4:
                continue
            try:
                vertex_buffer.append((float(parts[1]), float(parts[2]), float(parts[3])))
            except Exception:
                continue
            if len(vertex_buffer) == 3:
                base_index = len(vertices)
                vertices.extend(vertex_buffer)
                face_indices.append((base_index, base_index + 1, base_index + 2))
                vertex_buffer = []
        if len(face_indices) == 0:
            return None, None
        return np.asarray(vertices, dtype=float), np.asarray(face_indices, dtype=int)

    def _decode_binary_stl(self, content_bytes):
        if len(content_bytes) < 84:
            return None, None
        tri_count = struct.unpack('<I', content_bytes[80:84])[0]
        expected_len = 84 + tri_count * 50
        if expected_len > len(content_bytes):
            return None, None
        vertices = np.empty((tri_count * 3, 3), dtype=float)
        faces = np.empty((tri_count, 3), dtype=int)
        offset = 84
        for tri_index in range(tri_count):
            offset += 12
            for vertex_idx in range(3):
                x_value, y_value, z_value = struct.unpack('<fff', content_bytes[offset:offset + 12])
                vertices[tri_index * 3 + vertex_idx] = [x_value, y_value, z_value]
                offset += 12
            faces[tri_index] = [tri_index * 3, tri_index * 3 + 1, tri_index * 3 + 2]
            offset += 2
        return vertices, faces

    def _load_stl_vertices_faces(self, stl_path):
        with open(stl_path, 'rb') as stl_file:
            content_bytes = stl_file.read()
        vertices, faces = self._decode_binary_stl(content_bytes)
        if vertices is not None and faces is not None and len(faces) > 0:
            return vertices, faces
        return self._decode_ascii_stl(content_bytes)

    def _dedup_vertices_and_edges(self, vertices, faces):
        if vertices is None or faces is None or len(vertices) == 0:
            return None, None
        rounded = np.round(vertices, 6)
        unique_map = {}
        unique_vertices = []
        old_to_new = np.empty((len(vertices),), dtype=int)
        for idx, coord in enumerate(rounded):
            key = (coord[0], coord[1], coord[2])
            if key not in unique_map:
                unique_map[key] = len(unique_vertices)
                unique_vertices.append(vertices[idx])
            old_to_new[idx] = unique_map[key]
        edge_set = set()
        for face in faces:
            a_idx = old_to_new[int(face[0])]
            b_idx = old_to_new[int(face[1])]
            c_idx = old_to_new[int(face[2])]
            edge_set.add(tuple(sorted((a_idx, b_idx))))
            edge_set.add(tuple(sorted((b_idx, c_idx))))
            edge_set.add(tuple(sorted((c_idx, a_idx))))
        if len(edge_set) == 0:
            return None, None
        unique_vertices = np.asarray(unique_vertices, dtype=float)
        edge_array = np.asarray(sorted(edge_set), dtype=int)
        return unique_vertices, edge_array

    def _dedup_vertices_and_faces(self, vertices, faces):
        if vertices is None or faces is None or len(vertices) == 0:
            return None, None
        rounded = np.round(vertices, 6)
        unique_map = {}
        unique_vertices = []
        old_to_new = np.empty((len(vertices),), dtype=int)
        for idx, coord in enumerate(rounded):
            key = (coord[0], coord[1], coord[2])
            if key not in unique_map:
                unique_map[key] = len(unique_vertices)
                unique_vertices.append(vertices[idx])
            old_to_new[idx] = unique_map[key]

        new_faces = []
        for face in faces:
            mapped = [old_to_new[int(face[0])], old_to_new[int(face[1])], old_to_new[int(face[2])]]
            # 退化三角面不参与渲染
            if len(set(mapped)) < 3:
                continue
            new_faces.append(mapped)
        if len(new_faces) == 0:
            return None, None
        return np.asarray(unique_vertices, dtype=float), np.asarray(new_faces, dtype=int)

    def _normalize_vertices(self, vertices):
        center = np.nanmean(vertices, axis=0)
        centered = vertices - center
        max_len = np.nanmax(np.linalg.norm(centered, axis=1))
        max_len = max(max_len, 1e-6)
        return centered / max_len

    def _init_attitude_mesh(self):
        for stl_path in self._stl_paths():
            if not os.path.exists(stl_path):
                continue
            try:
                vertices, faces = self._load_stl_vertices_faces(stl_path)
                vertices, faces = self._dedup_vertices_and_faces(vertices, faces)
                if vertices is None or faces is None:
                    continue
                self._attitude_vertices = self._normalize_vertices(vertices)
                self._attitude_faces = faces
                _, edges = self._dedup_vertices_and_edges(self._attitude_vertices, self._attitude_faces)
                self._attitude_edges = edges
                self._attitude_has_stl = True
                self._set_attitude_status('姿态模型: {}'.format(os.path.basename(stl_path)))
                return
            except Exception as exc:
                self._append_nav_message('姿态模型加载失败 {}: {}'.format(stl_path, exc))

        # 兜底轮廓，保证未找到STL时姿态窗仍可更新。
        self._attitude_vertices = np.asarray([
            [0.0, 1.0, 0.0],
            [-0.35, -0.7, 0.18],
            [0.35, -0.7, 0.18],
            [0.0, -0.3, -0.28],
        ], dtype=float)
        self._attitude_faces = np.asarray([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3],
        ], dtype=int)
        self._attitude_edges = np.asarray([
            [0, 1], [0, 2], [1, 2], [0, 3], [1, 3], [2, 3]
        ], dtype=int)
        self._attitude_has_stl = False
        self._set_attitude_status('未找到aircraft.stl，使用简化姿态模型')

    def _ensure_gl_mesh_item(self):
        if not self._attitude_use_gl or self._attitude_gl_widget is None:
            return
        if self._attitude_vertices is None or self._attitude_faces is None:
            return
        if self._attitude_mesh_item is not None:
            return

        mesh_data = gl.MeshData(vertexes=self._attitude_vertices, faces=self._attitude_faces)
        self._attitude_mesh_item = gl.GLMeshItem(
            meshdata=mesh_data,
            drawEdges=False,
            drawFaces=True,
            smooth=False,
            shader='shaded',
            color=(0.35, 0.75, 0.95, 0.92),
        )
        self._attitude_mesh_item.setGLOptions('opaque')
        self._attitude_gl_widget.addItem(self._attitude_mesh_item)

    def _project_attitude_wireframe(self, pitch_deg, roll_deg, yaw_deg):
        if self._attitude_vertices is None or self._attitude_edges is None:
            return np.asarray([]), np.asarray([])

        pitch = np.deg2rad(float(pitch_deg))
        roll = np.deg2rad(float(roll_deg))
        yaw = np.deg2rad(float(yaw_deg))
        rx = np.asarray([
            [1.0, 0.0, 0.0],
            [0.0, np.cos(roll), -np.sin(roll)],
            [0.0, np.sin(roll), np.cos(roll)],
        ])
        ry = np.asarray([
            [np.cos(pitch), 0.0, np.sin(pitch)],
            [0.0, 1.0, 0.0],
            [-np.sin(pitch), 0.0, np.cos(pitch)],
        ])
        rz = np.asarray([
            [np.cos(yaw), -np.sin(yaw), 0.0],
            [np.sin(yaw), np.cos(yaw), 0.0],
            [0.0, 0.0, 1.0],
        ])
        rot = rz @ ry @ rx
        rotated = self._attitude_vertices @ rot.T
        projected = rotated[:, [0, 2]]

        x_values = []
        y_values = []
        for edge in self._attitude_edges:
            p0 = projected[int(edge[0])]
            p1 = projected[int(edge[1])]
            x_values.extend([p0[0], p1[0], np.nan])
            y_values.extend([p0[1], p1[1], np.nan])
        return np.asarray(x_values), np.asarray(y_values)

    def update_attitude_plot(self, pitch_deg, roll_deg, yaw_deg):
        self._attitude_last['pitch'] = float(pitch_deg)
        self._attitude_last['roll'] = float(roll_deg)
        self._attitude_last['yaw'] = float(yaw_deg)
        if self._attitude_use_gl:
            self._ensure_gl_mesh_item()
            if self._attitude_mesh_item is not None:
                self._attitude_mesh_item.resetTransform()
                # 按航向-俯仰-滚转顺序旋转，匹配现有数据定义。
                self._attitude_mesh_item.rotate(float(yaw_deg), 0, 0, 1)
                self._attitude_mesh_item.rotate(float(pitch_deg), 0, 1, 0)
                self._attitude_mesh_item.rotate(float(roll_deg), 1, 0, 0)
                if self._attitude_gl_widget is not None:
                    self._attitude_gl_widget.update()
            return

        x_values, y_values = self._project_attitude_wireframe(pitch_deg, roll_deg, yaw_deg)
        if self._attitude_wire_item is not None:
            self._attitude_wire_item.setData(x_values, y_values)
        model_tag = 'STL' if self._attitude_has_stl else 'Fallback'
        if self._attitude_label_item is not None:
            self._attitude_label_item.setText(
                '{}\nPitch:{:.2f}  Roll:{:.2f}  Yaw:{:.2f}'.format(model_tag, pitch_deg, roll_deg, yaw_deg)
            )

    def _parse_axis_value(self, axis_text, default_value=1):
        try:
            return int(str(axis_text).split()[0])
        except Exception:
            return int(default_value)

    def _axis_title(self, axis_index):
        if not hasattr(self.mw, 'sorted_titl_list'):
            return ''
        if axis_index < 0 or axis_index >= len(self.mw.sorted_titl_list):
            return ''
        return str(self.mw.sorted_titl_list[axis_index])

    def _axis_display_text(self, axis_index):
        title_text = self._axis_title(axis_index)
        return '{} {}'.format(axis_index, title_text).strip()

    def _read_optional_lineedit_text(self, object_name, fallback_value):
        editor = getattr(self.mw, object_name, None)
        if editor is None:
            return str(fallback_value)
        try:
            text_value = editor.text()
        except Exception:
            return str(fallback_value)
        text_value = str(text_value).strip()
        if len(text_value) == 0:
            return str(fallback_value)
        return text_value

    def _write_optional_lineedit_text(self, object_name, text_value):
        editor = getattr(self.mw, object_name, None)
        if editor is None:
            return
        try:
            editor.setText(str(text_value))
        except Exception:
            pass

    def _read_optional_combobox_tab_text(self, object_name, fallback_value):
        combo = getattr(self.mw, object_name, None)
        if combo is None:
            return str(fallback_value)
        try:
            current_text = str(combo.currentText()).strip()
        except Exception:
            return str(fallback_value)
        if len(current_text) == 0:
            return str(fallback_value)
        try:
            return current_text.split()[0]
        except Exception:
            return str(fallback_value)

    def _write_optional_combobox_tab_text(self, object_name, text_value):
        combo = getattr(self.mw, object_name, None)
        if combo is None:
            return
        try:
            combo.setCurrentText(str(text_value))
        except Exception:
            pass

    def _collect_imu_config_defaults(self):
        return {
            'target_tab': self._read_optional_combobox_tab_text('comboBox_INU_choiceTab_target', getattr(self.mw, 'inu_target_tab', 1)),
            'stand_tab': self._read_optional_combobox_tab_text('comboBox_INU_choiceTab_stand', getattr(self.mw, 'inu_stand_tab', 1)),
            'lon_col': str(getattr(self.mw, 'inu_lon_axis', 1)),
            'lat_col': str(getattr(self.mw, 'inu_lat_axis', 1)),
            'east_col': str(getattr(self.mw, 'inu_eastspd_axis', 1)),
            'north_col': str(getattr(self.mw, 'inu_northspd_axis', 1)),
            'up_col': str(getattr(self.mw, 'inu_upspd_axis', 1)),
            'stand_lon': str(getattr(self.mw, 'inu_stand_lon_text', '116.50271')),
            'stand_lat': str(getattr(self.mw, 'inu_stand_lat_text', '39.73155')),
            'radar_range': str(getattr(self.mw, 'inu_radar_distance_text', '500 1000 1500')),
            'stand_east_col': str(getattr(self.mw, 'inu_stand_east_text', '')),
            'stand_north_col': str(getattr(self.mw, 'inu_stand_north_text', '')),
            'stand_up_col': str(getattr(self.mw, 'inu_stand_up_text', '')),
            'pitch_col': str(getattr(self.mw, 'inu_pitch_axis', 1)),
            'roll_col': str(getattr(self.mw, 'inu_roll_axis', 1)),
            'yaw_col': str(getattr(self.mw, 'inu_yaw_axis', 1)),
            'skip_count': self._read_optional_lineedit_text('lineEdit_INU_skipcount', getattr(self.mw, 'inu_skip_count_text', '1')),
            'end_count': self._read_optional_lineedit_text('lineEdit_INU_endcount', getattr(self.mw, 'inu_end_count_text', '0')),
            'rolling': self._read_optional_lineedit_text('lineEdit_INU_rolling', getattr(self.mw, 'inu_rolling_text', '1')),
        }

    def _is_valid_axis(self, axis_index):
        if not hasattr(self.mw, 'sorted_titl_list'):
            return True
        return 0 <= axis_index < len(self.mw.sorted_titl_list)

    def _validate_config(self, config_dict):
        must_axis_fields = [
            'lon_col', 'lat_col', 'east_col', 'north_col', 'up_col',
            'pitch_col', 'roll_col', 'yaw_col'
        ]
        for field_name in must_axis_fields:
            axis_value = self._parse_axis_value(config_dict.get(field_name, ''), default_value=-1)
            if not self._is_valid_axis(axis_value):
                return False, '{} 列无效: {}'.format(field_name, config_dict.get(field_name, ''))
        for field_name in ['stand_east_col', 'stand_north_col', 'stand_up_col']:
            field_value = str(config_dict.get(field_name, '')).strip()
            if not field_value:
                continue
            axis_value = self._parse_axis_value(field_value, default_value=-1)
            if not self._is_valid_axis(axis_value):
                return False, '{} 列无效: {}'.format(field_name, config_dict.get(field_name, ''))
        return True, ''

    def apply_imu_config(self, config_dict):
        target_tab = max(1, self._parse_axis_value(config_dict.get('target_tab', '1'), 1))
        stand_tab = max(1, self._parse_axis_value(config_dict.get('stand_tab', '1'), 1))
        lon_axis = self._parse_axis_value(config_dict.get('lon_col', '1'), 1)
        lat_axis = self._parse_axis_value(config_dict.get('lat_col', '1'), 1)
        east_axis = self._parse_axis_value(config_dict.get('east_col', '1'), 1)
        north_axis = self._parse_axis_value(config_dict.get('north_col', '1'), 1)
        up_axis = self._parse_axis_value(config_dict.get('up_col', '1'), 1)
        pitch_axis = self._parse_axis_value(config_dict.get('pitch_col', '1'), 1)
        roll_axis = self._parse_axis_value(config_dict.get('roll_col', '1'), 1)
        yaw_axis = self._parse_axis_value(config_dict.get('yaw_col', '1'), 1)

        self.mw.inu_target_tab = target_tab
        self.mw.inu_stand_tab = stand_tab
        self.mw.inu_lon_axis = lon_axis
        self.mw.inu_lat_axis = lat_axis
        self.mw.inu_eastspd_axis = east_axis
        self.mw.inu_northspd_axis = north_axis
        self.mw.inu_stand_lon_text = str(config_dict.get('stand_lon', '116.50271')).strip()
        self.mw.inu_stand_lat_text = str(config_dict.get('stand_lat', '39.73155')).strip()
        self.mw.inu_radar_distance_text = str(config_dict.get('radar_range', '500 1000 1500')).strip()
        self.mw.inu_stand_east_text = str(config_dict.get('stand_east_col', '')).strip()
        self.mw.inu_stand_north_text = str(config_dict.get('stand_north_col', '')).strip()
        self.mw.inu_stand_up_text = str(config_dict.get('stand_up_col', '')).strip()
        self.mw.inu_skip_count_text = str(config_dict.get('skip_count', '1')).strip()
        self.mw.inu_end_count_text = str(config_dict.get('end_count', '0')).strip()
        self.mw.inu_rolling_text = str(config_dict.get('rolling', '1')).strip()

        self._write_optional_combobox_tab_text('comboBox_INU_choiceTab_target', target_tab)
        self._write_optional_combobox_tab_text('comboBox_INU_choiceTab_stand', stand_tab)
        self._write_optional_lineedit_text('lineEdit_INU_skipcount', self.mw.inu_skip_count_text)
        self._write_optional_lineedit_text('lineEdit_INU_endcount', self.mw.inu_end_count_text)
        self._write_optional_lineedit_text('lineEdit_INU_rolling', self.mw.inu_rolling_text)

        self.init_radar(fit_view=False)

        self.mw.inu_upspd_axis = up_axis
        self.mw.inu_pitch_axis = pitch_axis
        self.mw.inu_roll_axis = roll_axis
        self.mw.inu_yaw_axis = yaw_axis

        self._append_nav_message(
            'IMU列确认完成: 经{} 纬{} 东{} 北{} 天{} 基准东{} 基准北{} 俯{} 滚{} 航{}'.format(
                lon_axis,
                lat_axis,
                east_axis,
                north_axis,
                up_axis,
                self.mw.inu_stand_east_text or '-',
                self.mw.inu_stand_north_text or '-',
                pitch_axis,
                roll_axis,
                yaw_axis,
            )
        )

    def open_imu_config_dialog(self):
        title_list = getattr(self.mw, 'sorted_titl_list', [])
        dialog = IMUColumnConfigDialog(
            self.mw,
            defaults=self._collect_imu_config_defaults(),
            title_list=title_list,
        )
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return
        config_dict = dialog.get_config()
        valid_flag, valid_msg = self._validate_config(config_dict)
        if not valid_flag:
            QtWidgets.QMessageBox.warning(self.mw, 'IMU列确认', valid_msg)
            return
        self.apply_imu_config(config_dict)

    def _series_from_axis(self, data_frame, axis_index, skip_count, end_count, rolling):
        if data_frame is None or len(data_frame) == 0:
            return None
        if end_count == 0:
            series = data_frame.iloc[skip_count:, axis_index].reset_index(drop=True)
        else:
            series = data_frame.iloc[skip_count:-end_count, axis_index].reset_index(drop=True)
        rolling = max(1, int(rolling))
        if rolling > 1:
            series = series.rolling(rolling).mean()
        series = series.dropna()
        if len(series) == 0:
            return None
        return series

    def update_attitude_from_dataframe(self, data_frame, skip_count, end_count, rolling):
        pitch_axis = int(getattr(self.mw, 'inu_pitch_axis', 1))
        roll_axis = int(getattr(self.mw, 'inu_roll_axis', 1))
        yaw_axis = int(getattr(self.mw, 'inu_yaw_axis', 1))

        try:
            pitch_series = self._series_from_axis(data_frame, pitch_axis, skip_count, end_count, rolling)
            roll_series = self._series_from_axis(data_frame, roll_axis, skip_count, end_count, rolling)
            yaw_series = self._series_from_axis(data_frame, yaw_axis, skip_count, end_count, rolling)
            if pitch_series is None or roll_series is None or yaw_series is None:
                return
            self.update_attitude_plot(
                float(pitch_series.iloc[-1]),
                float(roll_series.iloc[-1]),
                float(yaw_series.iloc[-1]),
            )
        except Exception as exc:
            if hasattr(self.mw, 'debug_list_3'):
                self.mw.debug_list_3.append('{} 姿态更新失败:{}'.format(self.mw.normal_time, exc))
        
    def init_logic(self):
        self.mw.pushButton_standRe.setText('重载地图/雷达')
        self.mw.pushButton_standRe.setToolTip('重新读取 ./配置文件/map_config.ini，并适配当前导航视图')
        self.mw.pushButton_standRe.clicked.connect(self.reload_navigation_view)

        if hasattr(self.mw, 'pushButton_IMU_config'):
            self.mw.pushButton_IMU_config.setToolTip('确认经纬度/速度/基准/俯仰滚转航向列')
            self.mw.pushButton_IMU_config.clicked.connect(self.open_imu_config_dialog)
        if hasattr(self.mw, 'checkBox_lock'):
            self.mw.checkBox_lock.setChecked(bool(self._map_config.get('lock_aspect', True)))
            self.mw.checkBox_lock.toggled.connect(self.graphicsView_INU_loc_adp.setAspectLocked)
        
    def get_nav_msg(self):
        lat = str(getattr(self.mw, 'inu_stand_lat_text', '39.73155')).strip()
        lon = str(getattr(self.mw, 'inu_stand_lon_text', '116.31345')).strip()
        dis = str(getattr(self.mw, 'inu_radar_distance_text', '500 1000 1500')).strip()
        try: lat = float(lat)
        except: lat = 39.73155
        try: lon = float(lon)
        except: lon = 116.31345
        try: 
            list_dis = [float(d) for d in re.split('[,，\s]+', dis)]
        except: list_dis = [10,50,100]
        return lat, lon,list_dis

    # 初始化雷达图
    def init_radar(self, fit_view=True):
        lat, lon, list_dis = self.get_nav_msg()

        # 只保留有效的正距离，避免空输入或非法输入导致绘图异常。
        dis_values = []
        for d in list_dis:
            try:
                dv = float(d)
            except Exception:
                continue
            if dv > 0:
                dis_values.append(dv)

        if not dis_values:
            dis_values = [10.0, 50.0, 100.0]
        # 以经纬度为圆心，绘制多个距离圈，转换为经纬度格式

        # 仅刷新“距离圈”图层，不清空轨迹散点图层。
        for item in self._radar_circle_items:
            try:
                self.radar_adp.removeItem(item)
            except Exception:
                pass
        self._radar_circle_items = []

        if self._radar_ref_item is not None:
            try:
                self.radar_adp.removeItem(self._radar_ref_item)
            except Exception:
                pass
            self._radar_ref_item = None

        theta = np.linspace(0.0, 2.0 * np.pi, 361)
        lat_rad = np.deg2rad(lat)
        meter_per_deg_lat = np.pi * 6378137.0 / 180.0
        meter_per_deg_lon = meter_per_deg_lat * max(np.cos(lat_rad), 1e-6)

        max_r = max(dis_values)
        max_dlat = max_r / meter_per_deg_lat
        max_dlon = max_r / meter_per_deg_lon

        # 画同心圈：半径单位是米，坐标单位是经纬度。
        for r in sorted(set(dis_values)):
            dlat = r / meter_per_deg_lat
            dlon = r / meter_per_deg_lon
            circle_lon = lon + dlon * np.cos(theta)
            circle_lat = lat + dlat * np.sin(theta)
            circle_item = self.radar_adp.plot(
                circle_lon,
                circle_lat,
                pen=pg.mkPen(color=(0, 170, 255), width=1),
            )
            circle_item.setZValue(10)
            self._radar_circle_items.append(circle_item)

        # 圆心标记为基准经纬度，不影响定时更新的轨迹点。
        self._radar_ref_item = pg.ScatterPlotItem([lon], [lat], size=7, brush='y')
        self._radar_ref_item.setZValue(25)
        self.radar_adp.addItem(self._radar_ref_item)

        self.radar_adp.setLabel('left', 'Latitude', units='deg')
        self.radar_adp.setLabel('bottom', 'Longitude', units='deg')
        if self._map_item is None:
            self.radar_adp.setTitle(f"基准点: {lat:.6f}, {lon:.6f}")

        margin_lat = max(max_dlat * 0.15, 1e-5)
        margin_lon = max(max_dlon * 0.15, 1e-5)
        if fit_view:
            self.radar_adp.setXRange(lon - max_dlon - margin_lon, lon + max_dlon + margin_lon, padding=0)
            self.radar_adp.setYRange(lat - max_dlat - margin_lat, lat + max_dlat + margin_lat, padding=0)



