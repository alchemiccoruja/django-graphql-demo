import asyncio
from asgiref.sync import sync_to_async
from datetime import datetime
from graphene import ObjectType, String, Schema, Field

from django.shortcuts import get_object_or_404, render

from .models import Temperature, CurrentMeasurement


def _get_temperature(_pk):
    temperature = get_object_or_404(Temperature, pk=_pk)
    return temperature

get_temperature = sync_to_async(_get_temperature, thread_sensitive=True)


class CurrentTemperature(ObjectType):
    timestamp = String()
    value = String()
    unit = String()

    def resolve_timestamp(parent, info):
        print("resolve_timestamp - parent:, info: ".format(parent, info))
        return str(parent.latest_measurement().timestamp)
    
    def resolve_value(parent, info):
        print("resolve_value - parent:, info: ".format(parent, info))
        return str(parent.latest_measurement().value)
    
    def resolve_unit(parent, info):
        print("resolve_unit - parent:, info: ".format(parent, info))
        return str(parent.latest_measurement().unit)
 
class SubscribeCurrentTemperature(ObjectType):
    timestamp = String()
    value = String()
    unit = String()
    
    async def resolve_timestamp(parent, info):
        parent = _temperature =  await sync_to_async(get_object_or_404, thread_sensitive=True)(Temperature, pk = 1)
        latest_measurement =  await sync_to_async(parent.latest_measurement, thread_sensitive=True)()
        # print("async resolve_timestamp - parent: {},\n info: {} \n _temperature : {} \n latest_measurement: {}".format(
        #     parent, info, _temperature, latest_measurement)
        #     )
        return str(latest_measurement.timestamp)
    
    async  def resolve_value(parent, info):
        parent = _temperature =  await sync_to_async(get_object_or_404, thread_sensitive=True)(Temperature, pk = 1)
        latest_measurement =  await sync_to_async(parent.latest_measurement, thread_sensitive=True)()
        # print("async resolve_value - parent:, info: ".format(parent, info))
        return str(latest_measurement.value)
    
    async  def resolve_unit(parent, info):
        parent = _temperature =  await sync_to_async(get_object_or_404, thread_sensitive=True)(Temperature, pk = 1)
        latest_measurement =  await sync_to_async(parent.latest_measurement, thread_sensitive=True)()
        # print("async resolve_unit - parent:, info: ".format(parent, info))
        return  str(latest_measurement.unit)

class Query(ObjectType):
    current_temperature = Field(CurrentTemperature, timestamp = String(),  value = String(), unit = String())
    
    def resolve_current_temperature(root, info, timestamp, value,  unit):
        temperature = get_object_or_404(Temperature, pk=1)
        return temperature


class Subscription(ObjectType):
    time_of_day = String()
    current_temperature_subscribe = Field(SubscribeCurrentTemperature, timestamp = String(),  value = String(), unit = String())
    
    async def subscribe_time_of_day(root, info):
        while True:
            yield datetime.now().isoformat()
            await asyncio.sleep(1)
            
    async def subscribe_current_temperature_subscribe(root, info, timestamp = String(),  value = String(), unit = String()):
        while True:
            parent = {}
            yield parent
            await asyncio.sleep(1)
    


schema = Schema(query=Query, subscription=Subscription)


async def main(schema):
    #subscription = 'subscription { currentTemperatureSubscribe {  timestamp value   unit  } }'
    subscription = 'subscription { currentTemperatureSubscribe {  timestamp value   unit  } }'
    result = await schema.subscribe(subscription)
    async for item in result:
        print(item.data['currentTemperatureSubscribe'])