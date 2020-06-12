from loguru import logger
from . import constants
from . import TMW as tmw
from time import perf_counter
import datetime

"""
Build a multi-modal journey
"""


def filter_and_label_relevant_journey(journey_list):
    """
    We want to filter the most relevant journeys we want to display to the user
    We show the 3 cheapest, 3 fastest and 3 cleanest +
    we make sure that we have at least one journey of each type (if possible)
    """
    filtered_journeys = list()
    real_journeys = list(filter(lambda x: x.is_real_journey, journey_list))
    nb_journey_per_label = min(len(journey_list), 3)
    # Label the complete journeys
    real_journeys.sort(key=lambda x: x.total_price_EUR, reverse=False)
    real_journeys[0].label = constants.LABEL_CHEAPEST_JOURNEY
    filtered_journeys = filtered_journeys + real_journeys[0:nb_journey_per_label]
    journey_list.sort(key=lambda x: x.total_duration, reverse=False)
    journey_list[0].label = constants.LABEL_FASTEST_JOURNEY
    filtered_journeys = filtered_journeys + journey_list[0:nb_journey_per_label]
    journey_list.sort(key=lambda x: x.total_gCO2, reverse=False)
    journey_list[0].label = constants.LABEL_CLEANEST_JOURNEY
    filtered_journeys = filtered_journeys + journey_list[0:nb_journey_per_label]
    # logger.info(f'after labels we have {len(filtered_journeys)} journeys in the filter')
    # Making sure we hand out at least one journey for each type (if possible)
    type_checks = {constants.CATEGORY_COACH_JOURNEY: 0, constants.CATEGORY_TRAIN_JOURNEY: 0,
                   constants.CATEGORY_PLANE_JOURNEY: 0, constants.CATEGORY_CAR_JOURNEY: 0}
    for journey in journey_list:
        if (constants.CATEGORY_COACH_JOURNEY in journey.category) & (type_checks[constants.CATEGORY_COACH_JOURNEY] < 2):
            filtered_journeys.append(journey)
            type_checks[constants.CATEGORY_COACH_JOURNEY] = type_checks[constants.CATEGORY_COACH_JOURNEY] + 1
        if (constants.CATEGORY_TRAIN_JOURNEY in journey.category) & (type_checks[constants.CATEGORY_TRAIN_JOURNEY] < 2):
            filtered_journeys.append(journey)
            type_checks[constants.CATEGORY_TRAIN_JOURNEY] = type_checks[constants.CATEGORY_TRAIN_JOURNEY] + 1
        if (constants.CATEGORY_PLANE_JOURNEY in journey.category) & (type_checks[constants.CATEGORY_PLANE_JOURNEY] < 2):
            filtered_journeys.append(journey)
            type_checks[constants.CATEGORY_PLANE_JOURNEY] = type_checks[constants.CATEGORY_PLANE_JOURNEY] + 1
        if (constants.CATEGORY_CAR_JOURNEY in journey.category) & (type_checks[constants.CATEGORY_CAR_JOURNEY] < 2):
            filtered_journeys.append(journey)
            type_checks[constants.CATEGORY_CAR_JOURNEY] = type_checks[constants.CATEGORY_CAR_JOURNEY] + 1
    logger.info(f'after type check we have {len(filtered_journeys)} journeys in the filter')
    # Delete double entries
    return list(set(filtered_journeys))


def compute_complete_journey(departure_date = '2019-11-28', geoloc_dep=[48.85,2.35], geoloc_arrival=[43.60,1.44]):
    """
    Build a multi-modal journey:
    First we call each API to get a few journeys for each type of transportation
    Then we create a multi-modal trip by calling NAvitia between the departure point and departure station
        and between arrival station and arrival point.
    To limit the nb of Navitia calls, we first create all the necessary Navitia queries, and deduplicate them
        to make sure we call Navitia only once for each query
    Finally we call the filter function to choose which journeys we keep
    """
    # format date from %Y-%m-%dT%H:%M:%S.xxxZ without considering ms
    departure_date = datetime.datetime.strptime(str(departure_date)[0:19],"%Y-%m-%dT%H:%M:%S")
    # We only accept date up to 9 month in the future
    date_within_range = (datetime.datetime.today() + datetime.timedelta(days=9 * 30)) \
                            > departure_date
    if not date_within_range:
        raise Exception('Date out of range')
        # Let's create the start to finish query
    query_start_finish = tmw.Query(0, geoloc_dep, geoloc_arrival, departure_date)
    # logger.info(f'query_start_finish{query_start_finish.to_json()}')
    # Start the stopwatch / counter
    t1_start = perf_counter()
    # First we look for intercities journeys

    # Création des threads

    thread_trainline = tmw.ThreadComputeJourney(api='Trainline', query=query_start_finish)


    # Lancement des threads

    thread_trainline.start()


    # Attendre que les threads se terminent

    trainline_journeys, time_trainline = thread_trainline.join()



    if trainline_journeys is None:
        trainline_journeys = list()


    all_journeys = trainline_journeys

    nav_start = perf_counter()


    if len(all_journeys)>0:
        # Filter most relevant Journeys
        filtered_journeys = filter_and_label_relevant_journey(all_journeys)
        filtered_journeys = [filtered_journey.to_json() for filtered_journey in filtered_journeys]
    else :
        filtered_journeys = all_journeys
    t1_stop = perf_counter()
    logger.info(f'Elapsed time during computation: {t1_stop-t1_start} s')
    logger.info(f'including: {time_trainline}s for trainline ')
    return filtered_journeys


# This function only serves to run locally in debug mode
def main(departure_date='2020-05-28T10:00:00.540Z', geoloc_dep=[48.810553, 2.406533], geoloc_arrival=[43.6043, 1.44199]):
    all_trips = compute_complete_journey(departure_date, geoloc_dep, geoloc_arrival)
    logger.info(f'{len(all_trips)} journeys returned')
    for i in all_trips:
        logger.info(i)
        #print(i.to_json())

if __name__ == '__main__':
    main()
