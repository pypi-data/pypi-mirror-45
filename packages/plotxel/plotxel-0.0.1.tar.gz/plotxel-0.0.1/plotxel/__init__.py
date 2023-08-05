import svgwrite
from svgwrite import rgb
from math import log, floor
from collections import OrderedDict
import warnings
import cairosvg
#from warnings import Warning


def smart_limits(data):
    rounding_factor = .4
    head_room = .3
    true_max = max(abs(min(data)), abs(max(data)))
    num_zeros = log(rounding_factor * true_max, 10)
    limits = [0, 0]
    if max(data) == 0:
        limits[1] = 0
    else:
        limits[1] = round(max(data) + head_room * true_max, floor(num_zeros) * (-1))
    if limits[1] > 0 and max(data) < 0:
        limits[1] = 0
    if min(data) == 0:
        limits[0] = 0
    else:
        limits[0] = round(min(data) - head_room * true_max, floor(num_zeros) * (-1))
    if limits[0] < 0 and min(data) > 0:
        limits[0] = 0
    return limits


def smart_ticks(data, limits=None):
    if limits is None:
        limits = smart_limits(data)
    # print('Limits are: %s'%limits)
    # Ticks should only be in divisers of 1, 2, 2.5 or 5 and any 10x multiple of those, e.g. 10, 20, 25
    # We will start with ~ 5 ticks, but later adjust for axis size. We will also move this function to be an axis
    # class function

    # first, determine how many orders of magnitude our data spans
    magnitudes = floor(log(limits[1]-limits[0], 10))

    # next divide our limits by that
    div_limits = [limit/(10**magnitudes) for limit in limits]

    # manual, verbose checking potential limits to see how many ticks we would get
    potential_ticks = [.1, .2, .25, .5, 1, 2, 25, 50, 100]
    num_ticks = [floor((div_limits[1]-div_limits[0])/pt) for pt in potential_ticks]


    for i,num_tick in enumerate(num_ticks):
        # even though it says 3 to 6 allowed ticks, it's actually 4 to 7
        if (num_tick >= 3) & (num_tick <= 6):
            tick = potential_ticks[i]
            break

    # print("Tick value: %s %s times"%(tick*10**magnitudes, num_tick))
    # next, find the minimum tick value that matches out convention of allowable tick numbers
    tick = tick*10**magnitudes
    # subtract the remainder to the minimum, and we have our first tick
    first_tick = limits[0] - limits[0]%tick

    #propogate our ticks from there
    ticks = [first_tick]
    max_tick = first_tick

    while True:
        max_tick += tick
        #print(max_tick, limits[1])
        if max_tick > limits[1]:
            break
        else:
            ticks.append(max_tick)
    #print(ticks)
    return ticks


class Chart:
    def __init__(self, data_name):
        self.type = 'Chart'
        # chart properties
        self.dim = []  # [x, y] pixel size of graph. Does not include axes. Border will be truncated
        self.pos = []  # [x, y] pixels from top left corner
        self.xlim = []  # [min, max] limits of our x data
        self.ylim = []  # [min, max] limits of our y data
        #
        self.scale_to_inside_border = False
        self.inside_border_width = 1
        self.inside_border = [[1], [1], [1], [1]]  # top, right, bottom, left widths for the border
        self.inside_border_color = 'black'  # border color

        self.data_name = data_name  # the data we link our chart to

        # marker properties
        self.marker_shape = 'circle'
        self.marker_size = 5  # size of the markers, ideally this is the 'height' if the entire marker were contained
                              # in a square
        self.marker_fill_color = (50, 50, 200)  # color of the markers
        self.marker_border_color = (0, 0, 0)  # color of the marker border
        self.marker_border_width = 1  # thickness of the marker border. 0 means no border


    def get_x_res(self):
        return (self.dim[0]-1) / (self.xlim[1] - self.xlim[0])

    def get_y_res(self):
        return (self.dim[1]-1) / (self.ylim[1] - self.ylim[0])


class Scatter(Chart):
    def __init__(self, data):
        super().__init__(data)
        self.subtype = 'Scatter'


    def SetDefaults(self, data):
        pass

    def draw(self, main_figure):
        x_data = main_figure.data[self.data_name][0]
        y_data = main_figure.data[self.data_name][1]

        if not self.xlim:
            self.xlim = smart_limits(x_data)

        if not self.ylim:
            self.ylim = smart_limits(y_data)

        # make a figure the size of the main figure
        # we may need to draw outside of the actual chart area and into the main figure (for borders and such)
        # we also need to extract data series and other things
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0], main_figure.dim[1]))

        # determine how many pixels/value in our chart
        x_res = self.get_x_res()
        y_res = self.get_y_res()


        # establish our chart drawing area, such that the points are truncated if they fall outside the range
        # our chart points and circles will be added in here
        chart_area = svgwrite.Drawing(
            size=(self.dim[0], self.dim[1]),
            x=self.pos[0], y=self.pos[1])

        # each circle's position is calculated based on the chart size and it's data values
        # the points are plotted relative to our chart_area, which is then affixed to the main figure
        # x is plotted left to right. We calculate it by determining X's value relative to the chart minimum, then
        # multiplying it by the resolution to get it in pixels
        # y is plotted top to bottom, so same thing except we subtract the calculated value by the figure size
        # to get its proper position
        # future support: square, asterisk, dash, plus, custom svg

        for x, y in zip(x_data, y_data):

            center = (((x - self.xlim[0]) * x_res),
                      (self.dim[1] - (y - self.ylim[0]) * y_res))

            if self.marker_shape == 'circle':
                chart_area.add(
                    chart_area.circle(
                        #shape_rendering='crispEdges',
                        center=(center),
                        r=self.marker_size/2,
                        fill=rgb(self.marker_fill_color[0], self.marker_fill_color[1], self.marker_fill_color[2]),
                        stroke=rgb(self.marker_border_color[0], self.marker_border_color[1], self.marker_border_color[2],),
                        stroke_width=self.marker_border_width
                    )
                )
            elif self.marker_shape == 'square':
                chart_area.add(
                    chart_area.rect(
                        insert=(center[0] - self.marker_size/2, center[1] - self.marker_size/2),
                        size=(self.marker_size, self.marker_size),
                        fill=rgb(self.marker_fill_color[0], self.marker_fill_color[1], self.marker_fill_color[2]),
                        stroke=rgb(self.marker_border_color[0], self.marker_border_color[1],
                                   self.marker_border_color[2], ),
                        stroke_width=self.marker_border_width
                    )
                )

            elif self.marker_shape == 'rectangle' or self.marker_shape == 'rect':
                chart_area.add(
                    chart_area.rect(
                        insert=(center[0] - self.marker_size/2, center[1] - self.marker_size/4),
                        size=(self.marker_size, self.marker_size/2),
                        fill=rgb(self.marker_fill_color[0], self.marker_fill_color[1], self.marker_fill_color[2]),
                        stroke=rgb(self.marker_border_color[0], self.marker_border_color[1],
                                   self.marker_border_color[2], ),
                        stroke_width=self.marker_border_width
                    )
                )
            elif self.marker_shape == '-' or self.marker_shape == 'dash':
                pass
            elif self.marker_shape == '*' or self.marker_shape == 'star':
                pass




        # inside of our chart area we will add a border.
        if self.inside_border:
            if type(self.inside_border) == list:
                border_path = 'M '
                border_strokes = []
                for border_instruction in self.inside_border:
                    if border_instruction[0] == 1:
                        border_strokes.append('L')
                    else:
                        border_strokes.append('M')
                border_positions = []

                border_positions.append([0,
                                         int(self.inside_border_width/2) + self.inside_border_width % 2,
                                         ])

                border_positions.append([self.dim[0] - int(self.inside_border_width / 2),# + self.inside_border_width%2-1,
                                         int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                         ])

                border_positions.append([self.dim[0] - int(self.inside_border_width / 2),# + self.inside_border_width % 2-1,
                                         self.dim[1] - int(self.inside_border_width / 2)# + self.inside_border_width % 2-1
                                         ])

                border_positions.append([int(self.inside_border_width/2) + self.inside_border_width % 2,
                                         self.dim[1] - int(self.inside_border_width / 2)# + self.inside_border_width % 2-1
                                         ])

                border_positions.append([int(self.inside_border_width/2) + self.inside_border_width % 2,
                                         0
                                         ])


                border_strokes.append('M')
                print(border_positions)

                for stroke, border_position in zip(border_strokes, border_positions):
                    border_path += "%s %s %s" % (border_position[0], border_position[1], stroke)

                border_path += "%s %s" % (border_positions[0][0], border_positions[0][1])

                # print(border_path)
                chart_area.add(chart_area.path(border_path,
                                             shape_rendering='crispEdges',
                                             fill="none",
                                             stroke=self.inside_border_color,
                                             stroke_width=self.inside_border_width))
        subfigure.add(chart_area)
        return subfigure


class Histogram(Chart):
    pass


class Axis:
    def __init__(self, data_name, link_to):
        self.type = 'Axis'
        self.data_name = data_name
        self.dim = 0
        self.pos = []  # [x, y] svg pixel coordinates of bottom left of chart
        self.axis_offset = 0
        self.lim = []  # [min, max] limits of our axis
        self.color = rgb(0, 0, 0)  # color of our axis line

        self.major_tick_linewidth = 1
        self.major_tick_length = 5
        self.major_tick_color = rgb(0, 0, 0)
        self.major_ticks = []

        self.minor_tick_linewidth = 1
        self.minor_tick_color = rgb(0, 0, 0)

        self.axis_linewidth = 0

        self.tick_labels = []  # labels for our major ticks
        self.link_to = link_to
        self.text_offset_x = 0  # how far away the axis labels are away from the end of the ticks, y axis. 
        # Reverses if top/bottom or right/left axis
        self.text_offset_y = 0  # how far away the axis labels are away from the end of the ticks, x axis.
        # Reverses if top/bottom or right/left axis
        self.font_size = 10  # font size of the axis labels


class YAxis(Axis):
    def __init__(self, data_name=None, link_to=None):
        super().__init__(data_name, link_to)
        self.subtype = 'y'
        self.associated_drawable = ''
        self.side = 'left'


    def get_y_res(self):
        return (self.dim - 1) / (self.lim[1] - self.lim[0])

    def draw(self, main_figure):
        # grab any linked plot values
        # if there is a linked_chart and the values are not defined,
        # grab its data, its position, its dimensions and its limits
        if self.link_to:
            # print('establishing defaults')
            linked_chart = main_figure.drawables[self.link_to]
            if not self.data_name:
                self.data_name = main_figure.drawables[self.link_to].data_name

            if not self.pos:
                self.pos = main_figure.drawables[self.link_to].pos

            if not self.lim:
                self.lim = main_figure.drawables[self.link_to].ylim

            if not self.dim:
                self.dim = main_figure.drawables[self.link_to].dim[1]

            # print(self.data_name, self.pos, self.lim, self.dim)

        data = main_figure.data[self.data_name][1]
        tick_values = smart_ticks(data, self.lim)
        y_res = self.get_y_res()
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0],
                                           main_figure.dim[1]),
                                     style="text-anchor:end;font-size:%spx;font-style:arial;alignment-baseline:middle"%self.font_size)

        # start the svg path for the major tick
        major_tick_path = "M"

        if self.side == 'left':
            border_path = "M %s %s L %s %s" % (
                    self.pos[0] - self.axis_offset - self.axis_linewidth/2,
                    self.pos[1],
                    self.pos[0] - self.axis_offset - self.axis_linewidth/2,
                    self.pos[1] + self.dim)
            subfigure.add(subfigure.path(border_path, fill="none", stroke=self.color, stroke_width=self.axis_linewidth,
                                         shape_rendering='crispEdges'))

            for tick_value in tick_values:
                major_tick_path += " %s %s L %s %s M"%(
                    self.pos[0] - self.axis_offset,
                    self.pos[1] + self.dim - y_res * tick_value,
                    self.pos[0] - self.major_tick_length - self.axis_offset - self.axis_linewidth,
                    self.pos[1] + self.dim - y_res * tick_value)
            major_tick_path = major_tick_path[:-2]
            print('Y border path: ', major_tick_path)
            subfigure.add(subfigure.path(major_tick_path, fill="none", stroke=self.color,
                                         stroke_width=self.major_tick_linewidth,
                                         shape_rendering='crispEdges'))

            # label the ticks
            for tick_value in tick_values:
                x = self.pos[0] - self.major_tick_length - self.text_offset_x - self.axis_offset - self.axis_linewidth
                y = self.pos[1] + self.dim - y_res * tick_value + self.text_offset_y# + self.font_size/2.5
                subfigure.add(subfigure.text('%s'%tick_value,
                                             insert=(x, y)),)

        if self.side == 'right':
            #print('drawing a right axis')
            border_path = "M %s %s L %s %s" % (
                self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.axis_linewidth/2,
                self.pos[1],
                self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.axis_linewidth/2,
                self.pos[1] + self.dim)
            subfigure.add(subfigure.path(border_path, fill="none",
                                         stroke=self.color,
                                         stroke_width=self.axis_linewidth,
                                         shape_rendering='crispEdges'))
            for tick_value in tick_values:
                major_tick_path += " %s %s L %s %s M"%(
                    self.pos[0] + self.axis_offset + linked_chart.dim[0],
                    self.pos[1] + self.dim - y_res * tick_value,
                    self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.major_tick_length + self.axis_linewidth/2,
                    self.pos[1] + self.dim - y_res * tick_value)

            major_tick_path = major_tick_path[:-2]
            subfigure.add(subfigure.path(major_tick_path, fill="none", stroke=self.color,stroke_width=self.major_tick_linewidth,
                                         shape_rendering='crispEdges'))

            # label the ticks
            for tick_value in tick_values:
                x = self.pos[0] + self.major_tick_length + self.text_offset_x + self.axis_offset + \
                    linked_chart.dim[0] + self.axis_linewidth
                y = self.pos[1] + self.dim - y_res * tick_value + self.text_offset_y
                subfigure.add(
                    subfigure.text('%s' % tick_value,
                                   insert=(x, y),
                                   text_anchor="start"
                                   )
                )

        return subfigure

    def set_defaults(self, data):
        pass


class XAxis(Axis):
    def __init__(self, data_name=None, link_to=None):
        super().__init__(data_name, link_to)
        self.subtype = 'x'
        self.associated_drawable = ''
        self.side = 'bottom'

    def get_x_res(self):
        return (self.dim - 1) / (self.lim[1] - self.lim[0])


    def draw(self, main_figure):
        # write a function to grabbed any linked plot values
        # if there is a linked_chart and the values are not defined,
        # grab its data, its position, its dimensions and its limits
        chart_height = 0
        if self.link_to:
            #print('establishing defaults')
            if not self.data_name:
                self.data_name = main_figure.drawables[self.link_to].data_name

            if not self.pos:
                self.pos = [main_figure.drawables[self.link_to].pos[0],
                            main_figure.drawables[self.link_to].pos[1] + main_figure.drawables[self.link_to].dim[1]
                            ]

            if not self.lim:
                self.lim = main_figure.drawables[self.link_to].xlim

            if not self.dim:
                self.dim = main_figure.drawables[self.link_to].dim[0]

            chart_height = main_figure.drawables[self.link_to].dim[1]


            #print(self.data_name, self.pos, self.lim, self.dim)

        data = main_figure.data[self.data_name][0]
        tick_values = smart_ticks(data, self.lim)
        x_res = self.get_x_res()

        """
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0],
                                           main_figure.dim[1]),
                                     style="text-anchor:middle;font-size:%spx;font-style:arial;alignment-baseline:top"%self.font_size)
        """
        # draw the main axis. Might simply overlap with the figure border
        if self.side =='top':
            subfigure = svgwrite.Drawing(size=(main_figure.dim[0],
                                               main_figure.dim[1]),
                                         style="text-anchor:middle;font-size:%spx;font-style:arial;alignment-baseline:bottom" % self.font_size)
            border_path = "M %s %s L %s %s"%(self.pos[0],
                                             self.pos[1] - chart_height - self.axis_offset - self.axis_linewidth/2,
                                             self.pos[0] + self.dim,
                                             self.pos[1] - chart_height - self.axis_offset - self.axis_linewidth/2)

            subfigure.add(subfigure.path(border_path,
                                         fill="none",
                                         stroke=self.color,
                                         stroke_width=self.axis_linewidth,
                                         shape_rendering='crispEdges'))

            # draw the ticks
            major_tick_path = "M"
            for tick_value in tick_values:
                major_tick_path += " %s %s L %s %s M"%(
                    round(self.pos[0] + x_res * tick_value + 1),
                    round(self.pos[1] - chart_height - self.axis_offset),# + self.axis_linewidth/2,
                    round(self.pos[0] + x_res * tick_value + 1),
                    round(self.pos[1] - chart_height - self.major_tick_length - self.axis_offset - self.axis_linewidth))

            major_tick_path = major_tick_path[:-2]
            print('major tick path:', major_tick_path)
            subfigure.add(subfigure.path(major_tick_path,
                                         fill="none",
                                         stroke=self.color,
                                         stroke_width=self.major_tick_linewidth,
                                         shape_rendering='crispEdges'))

            # label the ticks


            for tick_value in tick_values:
                x = round(self.pos[0] + x_res * tick_value + self.text_offset_x),
                y = round(self.pos[1] - chart_height - self.major_tick_length - self.axis_offset - self.text_offset_y - self.axis_linewidth) # + self.font_size/2.5
                subfigure.add(subfigure.text('%s' % tick_value,
                                             insert=(x, y)), )

        if self.side =='bottom':
            subfigure = svgwrite.Drawing(size=(main_figure.dim[0],
                                               main_figure.dim[1]),
                                         style="text-anchor:middle;font-size:%spx;font-style:arial;alignment-baseline:top" % self.font_size)

            border_path = "M %s %s L %s %s"%(self.pos[0],
                                             self.pos[1] + self.axis_offset + self.axis_linewidth/2,
                                             self.pos[0] + self.dim,
                                             self.pos[1] + self.axis_offset + self.axis_linewidth/2)

            subfigure.add(subfigure.path(border_path,
                                         fill="none",
                                         stroke=self.color,
                                         stroke_width=self.axis_linewidth,
                                         shape_rendering='crispEdges'))

            # draw the ticks
            major_tick_path = "M"
            for tick_value in tick_values:
                major_tick_path += " %s %s L %s %s M"%(
                    self.pos[0] + x_res * tick_value + 1,
                    self.pos[1] + self.axis_offset,# + self.axis_linewidth/2,
                    self.pos[0] + x_res * tick_value + 1,
                    self.pos[1] + self.major_tick_length + self.axis_offset + self.axis_linewidth)

            major_tick_path = major_tick_path[:-2]

            subfigure.add(subfigure.path(major_tick_path,
                                         fill="none",
                                         stroke=self.color,
                                         stroke_width=self.major_tick_linewidth,
                                         shape_rendering='crispEdges'))

            # label the ticks
            for tick_value in tick_values:
                x = self.pos[0] + x_res * tick_value + self.text_offset_x
                y = self.pos[1] + self.major_tick_length + self.axis_offset + self.text_offset_y + self.axis_linewidth # + self.font_size/2.5
                subfigure.add(subfigure.text('%s' % tick_value,
                                             insert=(x, y)), )

        return subfigure


class Plotxel:
    def __init__(self, dim):
        self.dim = dim  # list, dimensions, in pixels, [width, height]
        self.data = {}  # dictionary to store all data values. will be referenced by data name
        self.drawables = OrderedDict()  # keep track of the drawable items (charts, axes) in the figure. each drawable has a name
        self.background_color = rgb(255, 255, 255)
        self.anti_aliasing = True

    def add_data(self, name, x, y):
        self.data[name] = [x, y]  # add some data. Drawables are linked to the data

    def add_drawable(self, drawable_name, drawable_type, data_name=None, link_to=None):
        """
        specify a data series name (in self.data), what kind of item, and its name
        """
        if drawable_type == "Scatter":
            self.drawables[drawable_name] = Scatter(data_name)

        elif drawable_type == "YAxis":
            self.drawables[drawable_name] = YAxis(data_name, link_to)

        elif drawable_type == "XAxis":
            self.drawables[drawable_name] = XAxis(data_name, link_to)
        elif drawable_type == 'XHist':
            print("XHist not implemented yet.")

        elif drawable_type == 'YHist':
            print("YHist not implemented yet.")

        else:
            warnings.warn("Could not create a drawable of '%s'. Acceptable inputs are 'Scatter', 'YAxis', 'XAxis', 'YHist', and 'XHist'"%drawable_type, Warning)

        return self.drawables[drawable_name]

    def draw(self):
        if self.anti_aliasing:
            svg_html = svgwrite.Drawing(size=(self.dim[0], self.dim[1]))
        else:
            svg_html = svgwrite.Drawing(size=(self.dim[0], self.dim[1]), shape_rendering='crispEdges')

        #svg_html = svgwrite.Drawing(size=(self.dim[0], self.dim[1]), shape_rendering='crispEdges')
        svg_html.add(svg_html.rect(size=(self.dim[0], self.dim[1]), fill=self.background_color, ))
        for figure_object_key in self.drawables:

            figure_object = self.drawables[figure_object_key]
            # check for our highest level objects. Chart, Axis, and we'll see what else in the future!!
            if figure_object.type == 'Chart':
                # print('Drawing a chart.')
                # if we encounter a Chart, it will have a subtype(e.g. Scatter) where 'draw' is defined.
                # we'll pass the object itself to the draw function so that we can extract the figure properties
                svg_html.add(figure_object.draw(self))
            if figure_object.type == 'Axis':
                # print('Drawing an axis.')
                svg_html.add(figure_object.draw(self))

        svg_html = svg_html.tostring()
        svg_html = svg_html.replace('><', '><')

        return svg_html
