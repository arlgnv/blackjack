from typing import Callable

import layers.view.types as ViewTypes
import layers.model.types as ModelTypes


EventName = ViewTypes.EventNames | ModelTypes.EventNames
Observers = dict[EventName, list[Callable[..., None]]]
