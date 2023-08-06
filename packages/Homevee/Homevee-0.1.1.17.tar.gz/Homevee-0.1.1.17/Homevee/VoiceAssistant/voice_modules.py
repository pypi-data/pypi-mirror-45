from Homevee.VoiceAssistant.Modules.CalendarModule.add_calendar_module import VoiceAddCalendarModule
from Homevee.VoiceAssistant.Modules.CalendarModule.get_calendar_module import VoiceGetCalendarModule
from Homevee.VoiceAssistant.Modules.DeviceControlModule.get_sensor_data_module import VoiceDeviceGetSensorDataModule
from Homevee.VoiceAssistant.Modules.DeviceControlModule.rgb_control_module import VoiceRgbDeviceControlModule
from Homevee.VoiceAssistant.Modules.DeviceControlModule.set_modes_module import VoiceDeviceSetModesModule
from Homevee.VoiceAssistant.Modules.ShoppingListModule.add_to_shopping_list_module import \
    VoiceAddToShoppingListModule
from Homevee.VoiceAssistant.Modules.ShoppingListModule.get_shopping_list_module import VoiceGetShoppingListModule
from Homevee.VoiceAssistant.Modules.add_nutrition_data_module import VoiceAddNutritionDataModule
from Homevee.VoiceAssistant.Modules.calculator_module import VoiceCalculatorModule
from Homevee.VoiceAssistant.Modules.conversation_module import VoiceConversationModule
from Homevee.VoiceAssistant.Modules.get_activities_module import VoiceGetActivitiesModule
from Homevee.VoiceAssistant.Modules.get_jokes_module import VoiceGetJokesModule
from Homevee.VoiceAssistant.Modules.get_nutrition_diary_module import VoiceGetNutritionDiaryModule
from Homevee.VoiceAssistant.Modules.get_nutrition_info_module import VoiceGetNutritionInfoModule
from Homevee.VoiceAssistant.Modules.get_recipes_module import VoiceGetRecipesModule
from Homevee.VoiceAssistant.Modules.get_summary_module import VoiceGetSummaryModule
from Homevee.VoiceAssistant.Modules.get_tv_schedule_module import VoiceGetTvScheduleModule
from Homevee.VoiceAssistant.Modules.get_tv_tipps_module import VoiceGetTvTippsModule
from Homevee.VoiceAssistant.Modules.get_weather_module import VoiceGetWeatherModule
from Homevee.VoiceAssistant.Modules.get_weekday_module import VoiceGetWeekdayModule
from Homevee.VoiceAssistant.Modules.get_wikipedia_definition import VoiceGetWikipediaDefinitionModule
from Homevee.VoiceAssistant.Modules.movie_api_module import VoiceMovieApiModule
from Homevee.VoiceAssistant.Modules.places_api_module import VoicePlacesApiModule


def get_voice_modules():
    voice_modules = [
        VoiceAddCalendarModule(priority=1),
        VoiceGetCalendarModule(priority=1),
        VoiceAddNutritionDataModule(priority=1),
        VoiceGetActivitiesModule(priority=1),
        VoiceGetNutritionInfoModule(priority=1),
        VoiceGetRecipesModule(priority=1),
        VoiceDeviceGetSensorDataModule(priority=1),
        VoiceGetSummaryModule(priority=1),
        VoiceGetTvScheduleModule(priority=1),
        VoiceGetTvTippsModule(priority=1),
        VoiceGetWeatherModule(priority=1),
        VoiceGetWeekdayModule(priority=1),
        VoiceGetWikipediaDefinitionModule(priority=1),
        VoiceGetJokesModule(priority=1),
        VoiceMovieApiModule(priority=1),
        VoiceGetNutritionDiaryModule(priority=1),
        VoicePlacesApiModule(priority=1),
        VoiceRgbDeviceControlModule(priority=1),
        VoiceDeviceSetModesModule(priority=1),
        VoiceAddToShoppingListModule(priority=1),
        VoiceGetShoppingListModule(priority=1),
        VoiceCalculatorModule(priority=1),
        VoiceConversationModule(priority=0),
        #VoiceModule(priority=1),
    ]

    #voice_modules = sorted(voice_modules, key=lambda x: x.get_priority(), reverse=True)

    return voice_modules