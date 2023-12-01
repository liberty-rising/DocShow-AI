
class NivoAssistant:
    """Assistant for working with the Nivo visualization library on the frontend."""
    def __init__(self, chart_type: str):
        self.chart_type = chart_type

    def sample_data_for_llm(self, nivo_config: dict, max_items: int = 5):
        """Shortens the data in the nivo config."""
        if not nivo_config:
            return None
        
        new_config = nivo_config
        new_config["data"] = nivo_config["data"][:max_items]
    
    def format_config(self, nivo_config: dict):
        if self.chart_type == 'bar':
            return self._format_bar_config(nivo_config)

    def _format_bar_config(self, nivo_config):
        # Define keys that are valid for bar configuration
        valid_keys = ['indexBy', 'keys', 'layout', 'margin', 'enableGridX', 'enableGridY', 'legends']

        # Filter nivo_config to only include valid keys
        filtered_config = {k: nivo_config[k] for k in valid_keys if k in nivo_config}

        return filtered_config

    def format_data(self, data: dict):
        if self.chart_type in ['bar', 'line', 'pie']:
            return data
        
    def get_available_params(self):
        if self.chart_type == 'bar':
            available_params = self.get_bar_params()
            return available_params
    
    def get_bar_params(self):
        """From https://nivo.rocks/bar/"""
        params = {
            "data":["object[] required", "Chart data."],
            "indexBy":["string | (datum: RawDatum): string | number optional default:'id'", 
                       "Key to use to index the data.",
                       "Key to use to index the data, this key must exist in each data item.", 
                       "You can also provide a function which will receive the data item and must return the desired index."
            ],
            "keys":[
                "string[] optional default:['value']", 
                "Keys to use to determine each serie."
            ],
            "groupMode":[
                "'grouped' | 'stacked' optional default:'stacked'",
                "stacked grouped", 
                "How to group bars."
            ],
            "layout":[
                "'horizontal' | 'vertical' optional default:'vertical'", 
                "horizontal vertical", 
                "How to display bars."
            ],
            "valueScale":{
                "valueScale":[
                    "object optional default:{\"type\":\"linear\"}", 
                    "value scale configuration."
                ],
                "valueScale.type":[
                    "string required",
                    "linear symlog",
                    "Scale type."
                ]
            },
            "indexScale":{
                "indexScale":[
                    "object optional default:{\"type\":\"band\",\"round\":true}",
                    "index scale configuration."
                ],
                "indexScale.type":[
                    "string required",
                    "band",
                    "Scale type."
                ],
                "indexScale.round":[
                    "boolean required",
                    "Toggle index scale (for bar width) rounding."
                ]
            },
            "reverse":[
                "boolean optional default:false",
                "Reverse bars, starts on top instead of bottom for vertical layout and right instead of left for horizontal one."
            ],
            "minValue":[
                "number | 'auto' optional default:'auto'",
                "Minimum value",
                "Minimum value, if 'auto', will use min value from the provided data."
            ],
            "maxValue":[
                "number | 'auto'optional default:'auto'",
                "Maximum value."
            ],
            "valueFormat":[
                "string | (value: number) => string | number optional",
                "Optional formatter for values.",
                "The formatted value can then be used for labels & tooltips.",
                "Under the hood, nivo uses d3-format, please have a look at it for available formats, you can also pass a function which will receive the raw value and should return the formatted one."
            ],
            "padding":[
                "number optional default:0.1",
                "Padding between each bar (ratio)."
            ],
            "innerPadding":[
                "number optional default:0",
                "Padding between grouped/stacked bars."
            ],
            "width":[
                "number required",
                "Chart width.",
                "Not required if using responsive component, <Responsive* />.",
                "Also note that width does not include labels/axes, so you should add enough margin to display them."
            ],
            "height":[
                "number required",
                "Chart height.",
                "Not required if using responsive component, <Responsive* />.",
                "Also note that height does not include labels/axes, so you should add enough margin to display them"
            ],
            "pixelRatio":[
                "number optional default:'Depends on device'",
                "Adjust pixel ratio, useful for HiDPI screens.",
                "support canvas"
            ],
            "margin":[
                "object optional",
                "Chart margin"
            ],
            "theme":[
                "Theme optional",
                "Define style for common elements such as labels, axes..."
            ],
            "colors":[
                "OrdinalColorScaleConfig optional default:{\"scheme\":\"nivo\"}",
                "Define chart's colors"
            ],
            "colorBy":[
                "'id' | 'indexValue'optional default:'id'",
                "Property used to determine node color."
            ],
            "borderRadius":[
                "number optional default:0",
                "Rectangle border radius."
            ],
            "borderWidth":[
                "number optional default:0",
                "Width of bar border."
            ],
            "borderColor":[
                "string | object | Function optional default:{\"from\":\"color\"}",
                "Method to compute border color."
            ],
            "defs":[
                "object[] optional",
                "Define patterns and gradients.",
                "support svg"
            ],
            "fill":[
                "object[] optional",
                "Define rules to apply patterns and gradients",
                "support svg"
            ],
            "layers":[
                "Array<string | Function> optional default:['grid', 'axes', 'bars', 'markers', 'legends', 'annotations']",
                "Defines the order of layers.",
                "support svg canvas",
                "Defines the order of layers, available layers are: grid, axes, bars, markers, legends, annotations. The markers layer is not available in the canvas flavor.",
                "You can also use this to insert extra layers to the chart, this extra layer must be a function which will receive the chart computed data and must return a valid SVG element."
            ],
            "enableLabel":[
                "boolean optional default:true",
                "Enable/disable labels."
            ],
            "label": [
                "string | Function optional default:'formattedValue'",
                "Define how bar labels are computed.",
                "By default it will use the bar's value. It accepts a string which will be used to access a specific bar data property, such as 'value' or 'id'.",
                "You can also use a funtion if you want to add more logic, this function will receive the current bar's data and must return the computed label which, depending on the context, should return a string or an svg element (Bar) or a string (BarCanvas). For example let's say you want to use a label with both the id and the value, you can achieve this with: label={d => `${d.id}: ${d.value}`}"
            ],
            "labelSkipWidth": [
                "number optional default:0",
                "Skip label if bar width is lower than provided value, ignored if 0."
            ],
            "labelSkipHeight": [
                "number optional default:0",
                "Skip label if bar height is lower than provided value, ignored if 0."
            ],
            "labelTextColor": [
                "string | object | Function optional default:",
                "{\"from\":\"theme\",\"theme\":\"labels.text.fill\"}",
                "Defines how to compute label text color."
            ],
            "enableGridX": [
                "boolean optional default:false",
                "Enable/disable x grid."
            ],
            "gridXValues": [
                "(number | string)[] optional",
                "Specify values to use for vertical grid lines."
            ],
            "enableGridY": [
                "boolean optional default:true",
                "Enable/disable y grid."
            ],
            "gridYValues": [
                "(number | string)[] optional",
                "Specify values to use for horizontal grid lines."
            ],
            "isInteractive": [
                "boolean optional default:true",
                "Enable/disable interactivity",
                "support svg canvas"
            ],
            "tooltip": [
                "Function optional",
                "Tooltip custom component",
                "support svg canvas",
                "A function allowing complete tooltip customisation, it must return a valid HTML element and will receive the following data: {bar: {id:             string | number,value:          number,formattedValue: string,index:          number,indexValue:     string | number,// datum associated to the current index (raw data)data:           object},color: string,label: string}"
            ],
            "legends": [
                "object[] optional",
                "Optional chart's legends."
            ]
        }
        return params