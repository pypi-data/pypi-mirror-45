from __future__ import absolute_import

import logging

from .base import FEIWSBaseClient


logger = logging.getLogger('fei-ws.client')


#TODO implement Commen WebService Method in client
#TODO refactor client11 to just client


class FEIWSClient(FEIWSBaseClient):
    def __init__(self, username=None, password=None):
        logger.info('initialize FEI WS Client')
        super(FEIWSClient, self).__init__((1, 2), username, password)

    def find_athlete(self, fei_ids=None, family_name=None, first_name=None,
                     gender_code=None, competing_for=None):
        """
        Find athletes based on a certain search criteria.
        :param fei_ids: A tuple of Athlete FEI IDs you want to search for.
        :param family_name: The athlete's family name. Use % to create a `contain` query
        :param first_name: The athlete's first name. User % to create a `contain` query
        :param gender_code: The athlete gender(None=All, M=Male, F=Female)
        :param competing_for: The NOC code of the athlete's country he is competing for
        :return: An array of Athlete objects.
        """
        fei_ids_array = None
        if fei_ids:
            fei_ids_array = self._ows_factory.ArrayOfString(string=fei_ids)
        result = self.get_organizer_data('findAthlete',
            FEIIDs=fei_ids_array, FamilyName=family_name, FirstName=first_name,
            GenderCode=gender_code, CompetingFor=competing_for)
        return result.AthleteOC if hasattr(result, 'AthleteOC') else []

    def find_official(self, any_id=None, any_name=None, person_gender=None,
                     admin_nf=None, person_status=None, official_function=None,
                     official_function_discipline=None):
        """
        Find officials based on a certain search criteria.
        :param any_id: Return officials having this ID, licence nr, or vet delegat nr.
        :param any_name: Return officials having this family name, first name, nick name.
            use % to make a `contain` search.
        :param person_gender: Return officials with this gender (None=All, M=Male, F=Female)
        :param admin_nf: Return official that are member of the administrative NF
        :param person_status: Return the official having this status:
                10: Search for all competitors
                1: Search only for active competitors
                0: Search only for inactive competitors
                2: Search only for pending competitors
                3: Search only for cancelled competitors
                9: Search only for suspended competitors.
        :param official_function: Search for officials with specified function
        :param official_function_discipline: Return officials having the specified official
                function for this discipline.
        :return: An array of PersonOfficialOC objects
        """
        result = self.get_organizer_data('findOfficial',
            AnyID=any_id, AnyName=any_name, PersonGender=person_gender, AdminNF=admin_nf,
            PersonStatus=person_status, OfficialFunction=official_function,
            OfficialFunctionDiscipline=official_function_discipline)
        if hasattr(result, 'PersonOfficialOC'):
            return result.PersonOfficialOC
        return []

    def find_horse(self, fei_ids=None, name=None, sex_code=None, is_pony=None,
                   athlete_fei_id=None):
        """
        Find horses based on a certain search criteria.
        :param fei_ids: A tuple of Horse FEI IDs you want to search for.
        :param name: The name of the horse. Use % to create a contain query
        :param sex_code: The sex code of the horse (None=All, F=Mare, G=Gelding,
                S=Stallion, M=Male Unknown, U=Unknown).
        :param is_pony: Boolean indicating to search for only ponies.
        :param athlete_fei_id: Search for horses associated with this Athlete.
        :return: A list of Horse objects.
        """
        fei_ids_array = None
        if fei_ids:
            fei_ids_array = self._ows_factory.ArrayOfString(string=fei_ids)
        result = self.get_organizer_data('findHorse',
            FEIIDs=fei_ids_array, Name=name, SexCode=sex_code, IsPony=is_pony,
            AthleteFEIID=athlete_fei_id)
        return result.HorseOC if hasattr(result, 'HorseOC') else []

    def search_horse_trainers(self, horse_fei_code=None, person_fei_id=None, eval_date=None, page_number=1):
        """
        Search for horse trainer records

        :param horse_fei_code: The FEI identifier of the horse filters the records and returns only trainers
        linked to this horse. It maybe null.
        :param person_fei_id: The FEI identifier of the person filters the records and returns only the trainer
        having this ID. It may be null
        :param eval_date: The evaluation date filters the horse trainer records and returns only those whose period
        is active at this evaluation date. It may be null.
        :param page_number: Which page to retrieve. 1 = 1 - 100, 2 = 101 - 200
        :return: returns an array of zero or more HorseTrainer objects.
        """

        result = self.get_organizer_data('searchHorseTrainers',
            HorseFEICode=horse_fei_code, PersonFEIID=person_fei_id, EvalDate=eval_date, PageNumber=page_number)
        if hasattr(result, 'HorseTrainer'):
            return result.HorseTrainer
        return[]

    def find_event(self, id='', show_date_from=None, show_date_to=None, venue_name='', nf='', discipline_code='',
                   level_code='', is_indoor=None):
        """
        Find FEI events based on a certain search criteria.
        :param id: FEI show/event/competition ID.
        :param show_date_from: Filter shows from this date up.
        :param show_date_to: Filter shows from this date down.
        :param venue_name: The name of the place where the show is held.
        :param nf: Country code of the national federation.
        :param discipline_code: Filter shows based on discipline.
        :param level_code: Filter shows based on level.
        :param is_indoor: Filter indoor / outdoor shows.
        :return: Return value: A list of FEI events
        """
        result = self.get_organizer_data(
            'findEvent',
            ID=id, ShowDateFrom=show_date_from, ShowDateTo=show_date_to, VenueName=venue_name, NF=nf,
            DisciplineCode=discipline_code, LevelCode=level_code, IsIndoor=is_indoor)
        if hasattr(result, 'ShowOC'):
            return result.ShowOC
        return []

    def download_results(self, id):
        """
        Download XML results from the FEI. (You need permission from the FEI
         to download results from an event.
        :param id: FEI event/competition ID.
        :return: A string containing the information in FEI XML.
        """
        result = self._ows_client.service.downloadResults(id)
        self._handle_messages(result)
        return result

    def upload_results(self, result_xml_data):
        """
        Upload results to the FEI. (You need permission from the FEI to
        upload results to the FEI.
        :param result_xml_data: Base64Encoded FEI result file.
        :return:
            FileID = can be used to confirm uploaded results
            Results = String indicating if the uploaded succeeded.
                ERR = An error was found while processing the validation
                MAN = An error was found while processing the mandotory check
                OKW = It is ok for saving, but there are warnings
                OKD = the saving has been done
        """
        return self._ows_client.service.uploadResults(result_xml_data)

    def confirm_upload_results(self, file_id):
        """
        Confirm uploaded results. This is only needed when results returned OK with warnings.
        :param file_id: The FileID return by the uploadResults routine.
        :return: True if the saving has been done.
        """
        return self._ows_client.service.confirmUploadResults(file_id)

    def submit_results(self, id):
        """
        Submit the results to the FEI validation for a given event or a
         given competition.
        :param id: FEI event/competition ID.
        :return: True if the results have been successfully submitted.
        """
        return self._ows_client.service.submitResults(id)

    def get_version(self):
        """
        Return the version string of the Core Application software
        :return: Returns a string containing the [major.minor.revision] number.
        If no return value is recieved or the call times out then the web service is not working
        and should not be used.
        """
        return self.get_common_data('getVersion')

    def get_lookup_date_list(self):
        """
        Retrieve a list of cached information types, and the date each was last modified.
        :return: Returns an array of LookupDate objects.
        Each LookupDate object contains the name of an object type and the most recent date of modification
        for any of the lookup records held in that object type. Client applications should keep these
        lookup records in a local cache to improve performance, and reduce server load.
        For each of these LookupDate objects, there is a corresponding method get<LookupDate.Name>List()
        that retrieves a list of all records of that type.
        """
        result = self.get_common_data('getLookupDateList')
        return result.LookupDate


    def get_country_list(self):
        """
        Retrieve a list of countries.
        :return: Returns an array of Country objects.
        Returns an array of Country objects containing all countries and their corresponding
        names and nationally recognized codes (NOC).
        """
        result = self.get_common_data('getCountryList')
        return result.Country

    def get_dicipline_list(self):
        """
        Retrieve a list of discipline records
        :return: Returns an array of Discipline objects.
        """
        result = self.get_common_data('getDisciplineList')
        return result.Discipline

    def get_issuing_body_list(self):
        """
        Retrieve a list of document issuing bodies.
        :return: Returns an array of DocIssuingBody objects.
        """
        result = self.get_common_data('getDocIssuingBodyList')
        return result.DocIssuingBody

    def get_national_federation_list(self):
        """
        Retrieve a list of National Federations.
        :return: Returns an array of NationalFederation objects.
        """
        result = self.get_common_data('getNationalFederationList')
        return result.NationalFederation

    def get_horse_name_kind_change_list(self):
        """
        Retrieve a list of kind of changes for the name of a horse.
        :return: Returns an array of KindChange objects.
        """
        result = self.get_common_data('getHorseNameKindChangeList')
        return result.KindChange

    def get_document_type_list(self):
        """
        Retrieve a list of extension for the document type.
        :return: Returns an array of DocumentType objects.
        """
        result = self.get_common_data('getDocumentTypeList')
        return result.DocumentType

    def get_language_list(self):
        """
        Retrieve a list of languages used for mailings.
        :return: Returns an array of Language objects.
        """
        result = self.get_common_data('getLanguageList')
        return result.Language

    def get_category_list(self):
        """
        Retrieve a list of categories for an event.
        :return: Returns an array of Category objects containing all
        category values and their corresponding names.
        """
        result = self.get_common_data('getCategoryList')
        return result.Category

    def get_address_name_list(self):
        """
        Retrieve a list of address types.
        :return: Returns an array of AddressName objects containing all addresstypes.
        """
        result = self.get_common_data('getAddressNameList')
        return result.AddressName

    def get_horse_gender_list(self):
        """
        Retrieve a list of horse genders.
        :return: Returns an array of Gender objects containing all horse genders.
        """
        result = self.get_common_data('getHorseGenderList')
        return result.Gender

    def get_horse_fei_id_type_list(self):
        """
        Retrieve a list of horse FEI ID types.
        :return: Returns an array of FEIIDType objects containing all horse FEI ID types.
        """
        result = self.get_common_data('getHorseFEIIDTypeList')
        return result.FEIIDType

    def get_person_gender_list(self):
        """
        Retrieve a list of person genders.
        :return: Returns an array of Gender objects containing all person genders.
        """
        result = self.get_common_data('getPersonGenderList')
        return result.Gender

    def get_person_civility_list(self):
        """
        Retrieve a list of person civilities.
        :return: Returns an array of Person Civility objects containing all person civilities.
        """
        result = self.get_common_data('getPersonCivilityList')
        return result.Civility

    def get_official_function_list(self):
        """
        Retrieve a list of official functions.
        :return: Returns an array of OfficialFunction objects containing all additional functions.
        """
        result = self.get_common_data('getOfficialFunctionList')
        return result.OfficialFunction

    def get_official_status_list(self):
        """
        Retrieve a list of official status.
        :return: Returns an array of OfficialStatus objects containing all additional status.
        """
        result = self.get_common_data('getOfficialStatusList')
        return result.OfficialStatus

    def get_additional_role_list(self):
        """
        Retrieve a list of additional roles.
        :return: Returns an array of AdditionalRole objects containing all additional roles.
        """
        result = self.get_common_data('getAdditionalRoleList')
        return result.AdditionalRole

    def get_message_type_list(self):
        """
        Retrieve a list of error message types and warnings.
        :return: Returns an array of MessageType objects.
        """
        result = self.get_common_data('getMessageTypeList')
        return result.MessageType

    def get_season_list(self, discipline_code='S'):
        """
        Returns the list of World Cup seasons for a given discipline
        (jumping and dressage seasons, currently).
        Those season strings can then be used as input in getLeagueList.
        :param discipline_code: Specify which World Cup seasons will be returned:
            S for World Cup Jumping seasons and D for World Cup Dressage seasons.
        :return: The method returns an array of strings corresponding each
        to a World Cup season of the chosen discipline.
        """
        result = self.get_common_data('getSeasonList', DisciplineCode=discipline_code)
        return result.string

    def get_league_list(self, discipline_code='S', season_code=None):
        """
        Returns a list of Leagues for a given discipline and season
        :param discipline_code: Specify which World Cup leagues will be returned:
            S for World Cup Jumping leagues and D for World Cup Dressage leagues.
        :param season_code: Specify a World Cup season.
            Only the leagues valid during this season will be returned.
        :return: The method returns an array of strings corresponding each to a World Cup
            league of the chosen discipline.
        """
        result = self.get_common_data('getLeagueList', DisciplineCode=discipline_code,
                                      SeasonCode=season_code)
        return result.League
