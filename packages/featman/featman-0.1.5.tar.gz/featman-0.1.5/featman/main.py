# Gets the latest or given time featrues
import time
from copy import copy


import dask
import pandas as pd
import toolz as tz
import maya
from crayons import blue, green, red, yellow, cyan
from spaceman import Spaceman
from loguru import logger

"""
    # How Features Will Work
    ---

    ```
        features = (
            Features(host="localhost", db="global")
                .set_storage("...")
                .set_type('...')
                .set_time(now=False, back=True, month=0, day=0, hour=0, minute=30)
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .set_data(dataframe: pd.Dataframe, time_index=True, scale="minute")
                .save()
        )
	
	data = features.load()
    ```
"""


class Features(object):
    def __init__(self):
        self.parameters = {
            "type": "general"
        }
        self.acceptable = [str, int, float, complex, list, tuple, dict, object]
        self.data_list = []
        self.space = Spaceman()
        self.merged = None
        self.generic_data = None
        self.current_time = maya.now()

    def set_storage(self, **kwargs):
        return self

    def set_type(self, _type, **kwargs):
        if not isinstance(_type, str):
            raise TypeError(f"The type - `{_type}` you entered isn't a `str`")
        # print({'type': _type})
        self.parameters.update({'type': _type})

        return self

    def set_time(self, **kwargs):

        is_now = kwargs.get("is_now", True)
        before_now = kwargs.get("before_now", True)
        after_now = kwargs.get("after_now", True)
        _months = kwargs.get("_months", 0)
        _days = kwargs.get("_days", 0)
        _hours = kwargs.get("_hours", 0)
        _minutes = kwargs.get("_minutes", 0)
        _seconds = kwargs.get("_seconds", 30)
        
        # logger.info(f"Set Time Parameters: is_now={is_now}, before_now={before_now}, after_now={after_now}, months={_months}, days={_days}, hours={_hours}, minutes={_minutes}, seconds={_seconds}")

        if is_now == True and (before_now == False and after_now == False):
            self.current_time = maya.now()
            # print(self.current_time)
            # logger.info(self.current_time)
        elif before_now == True:
            self.current_time = maya.now()
            self.current_time = self.current_time.subtract(
                months=_months, days=_days, hours=_hours, minutes=_minutes, seconds=_seconds
            )
            # logger.info(self.current_time)
        elif after_now == True:
            self.current_time = maya.now()
            self.current_time = self.current_time.add(
                months=_months, days=_days, hours=_hours, minutes=_minutes, seconds=_seconds
            )
            # logger.info(self.current_time)

        return self

    def add_parameter(self, k, v):
        if type(v) not in self.acceptable:
            raise TypeError(f"Value type not acceptable {self.acceptable}")
        if (not isinstance(k, str)):
            raise TypeError("The key is not a `str`")

        self.parameters.update({k: v})
        return self

    def add_data(self, data: pd.DataFrame, ts_index=True, **kwargs):
        if isinstance(data, pd.DataFrame):
            self.data_list.append(data)
        else:
            raise TypeError("data is not a `DataFrame`")
        return self
    
    def add_generic(self, data):
        self.generic_data = data
        return self

    def smart_merge(self):
        """ Smart merge things together """

        if len(self.data_list) > 0:
            total = (
                tz.reduce(
                    lambda x, y: pd.merge(
                        x, y, how='outer', left_index=True, right_index=True),
                    self.data_list
                )
            )

            self.merged = total

    def prepare_parameters(self):
        self.smart_merge()
        self.parameters.update(
            {"timestamp": self.current_time.__dict__["_epoch"]}
        )

        
    
    def load_prep(self):
        name = self.parameters.get("name")
        filename = self.parameters.get("filename")
        loc = self.parameters.get("loc")
        provider = self.parameters.get("provider")

        if name is not None:
            del self.parameters["name"]
        if filename is not None:
            del self.parameters["filename"]
        if loc is not None:
            del self.parameters["loc"]
        if provider is not None:
            del self.parameters["provider"]

        # logger.info(f"The parameters are: {self.parameters}")
    def print_parameters(self):
        print(self.parameters)
    
    def reset(self):
        self.generic_data = None
        self.merged = None
        self.data_list = []
        return self
        

    def save(self, _type="df", is_now=True):
        """ Get the parameters and save it. """

        self.prepare_parameters()
        # self.print_parameters()

        if is_now:
            self.current_time = maya.now()
            self.parameters.update(
                {"timestamp": self.current_time.__dict__["_epoch"]}
            )
        # print(red(self.parameters))
        # print(f"Save Time: {self.parameters['timestamp']}")
        with self.space as space:
            if _type == "df":
                if self.merged is None:
                    logger.debug("No merged value. Exiting save")
                    return None
                try:
                    self.parameters['dtype'] = "main"
                    space.store(self.merged, query=self.parameters, current_time=is_now)
                except Exception as e:
                    logger.exception(e)
                    return None
            elif _type == "generic":
                if self.generic_data is None:
                    logger.error("No genetic data. Exiting save")
                    return None
                try:
                    self.parameters['dtype'] = "generic"
                    space.store(self.generic_data, query=self.parameters, current_time=is_now)
                    return self.generic_data
                except Exception as e:
                    logger.exception(e)
                    return None
        return self.merged

    def load(self, _type="df", is_now=True, is_before=True):
        """ Pull data according to what parameters say from the database """
        self.prepare_parameters()
        self.load_prep()
        if is_now:
            self.current_time = maya.now()
            self.parameters.update(
                {"timestamp": self.current_time.__dict__["_epoch"]}
            )
        # print(yellow(self.parameters))
        # print(f"Load Time: {self.parameters['timestamp']}")
        with self.space as space:
            if _type == "df":
                try:
                    self.parameters['dtype'] = "main"
                    # get_latest=is_now, 
                    # print(green(self.parameters))
                    self.merged = space.load(query=self.parameters, already_shifted=(not is_now), is_before=is_before)
                except Exception as e:
                    logger.exception(e)
                    return None
            elif _type == "generic":
                try:
                    self.parameters['dtype'] = "generic"
                    self.merged = space.load(query=self.parameters, already_shifted=(not is_now), is_before=is_before)
                except Exception as e:
                    logger.exception(e)
                    return None
        return self.merged


fd = [{"type": "one", "way": 1234}, {"type": "one", "way": 1234}]


def run_feature_address():
    """ Run the folder """
    features = (Features()
                .set_type("world")
                .set_type("hollow")
                .set_time(is_now=True, before_now=False, after_now=False)
                .set_storage()
                .add_parameter("four", 3)
                .add_parameter("three", 4)
                .add_data(pd.DataFrame(fd))
                .save())
    print(yellow(features))

    complex_item = (Features()
                    .set_type("mego")
                    .set_time(is_now=True, before_now=False, after_now=False)
                    .set_storage()
                    .add_parameter("four", 3)
                    .add_parameter("three", 4)
                    .add_generic({"big": "dick"})
                    .save(_type="generic"))

    complex_loaded = (Features()
                        .set_type("mego")
                        .set_time(is_now=True, before_now=False, after_now=False)
                        .set_storage()
                        .add_parameter("four", 3)
                        .add_parameter("three", 4)
                        .add_generic({"big": "dick"})
                        .load(_type="generic")
                    )
    print(complex_item)
    print(complex_loaded)


if __name__ == "__main__":
    run_feature_address()

