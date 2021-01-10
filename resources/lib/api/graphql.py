import requests
from .models import Video, PlayBack, Serie, Page, Structure
from resources.lib.logging import LOG

class GraphQL_API():
    def __init__(self):
        self.api_url = "https://api.ovp.tv2.dk"

    def __get_headers(self, access_token):
        headers = {
            "Authorization": access_token
        }
        return headers
    
    def __do_request(self, query, headers={}, **kwargs):
        data = {"query": query, "variables": kwargs}
        response = requests.post(self.api_url, json=data, headers={})
        response_data = response.json()["data"]
        if response.status_code == 200 and response_data != None:
            return response_data
        return None

    def get_subpages(self, page_path):
        query = """
            query PageQuery($path: String!, $limit: Int){
                    page(path: $path, platform: play_web){
                id
                title
                subpages(limit: $limit) {
                  nodes {
                    title
                    id
                    path
                  }
                }
              }
            }
        """
        data = self.__do_request(query, path=page_path, limit=20)["page"]["subpages"]
        if data != None:
            pages = []
            for p in data["nodes"]:
                pages.append(Page(p))
            return pages
        return []
    
    def get_structures(self, page_path):
        query = """
            query PageQuery($path: String!){
                    page(path: $path, platform: play_web){
                id
                title
                structures {
                  nodes {
                    title
                    id
                  }
                }
              }
            }
        """
        structures = []
        data = self.__do_request(query, path=page_path)["page"]
        if data["structures"] != None:
            for s in data["structures"]["nodes"]:
                structures.append(Structure(s))
        return structures

    def get_series(self, structure_id):
        sort = "popular"
        query = """
            query play_web_content_Structure(
              $entitySort: SortType
              $structureId: ID!
              $limit: Int
            ) {
              structure(id: $structureId) {
                ...StructureFragment
              }
            }
            fragment StructureFragment on Structure {
              entities(
                sort: $entitySort
                limit: $limit
              ) {
                pageInfo {
                  totalCount
                }
                nodes {
                  ...StructureEntityFragment
                }
              }
            }

            fragment StructureEntityFragment on Entity {
              id
              guid
              type
              title: presentationTitle
              description: presentationDescription
              thumbnail: presentationArt {
                type
                url
              }
              ... on Episode {
                art(type: "promotion") {
                  nodes {
                    url
                    watermarkParam
                  }
                }
              }
            }
        """
        variables = {"limit": 9999, "entitySort": sort, "structureId": structure_id}
        data = {"query": query, "variables": variables}
        response = requests.post(self.api_url, json=data)
        if response.status_code == 200:
            series = []
            for s in response.json()["data"]["structure"]["entities"]["nodes"]:
                series.append(Serie(s))
            return series
        return None
    
    def get_videos(self, serie_guid):
        query = """
            query play_web_content_SeriesEpisodeEntityPage_LatestEpisodes(
              $seriesGuid: String!
              $limit: Int
            ) {
              series: entity(type: series, guid: $seriesGuid) {
                ... on Series {
                  episodes(limit: $limit) {
                    ...EpisodeListFragment
                  }
                }
              }
            }
            fragment EpisodeListFragment on EpisodeList {
              pageInfo {
                totalCount
              }
              nodes {
                episodeNumber
                firstPublicationDate
                lastPublicationDate
                watched
                ... on Progressable {
                  progress {
                    position
                    duration
                  }
                }
                ...StructureEntityFragment
              }
            }
            fragment StructureEntityFragment on Entity {
              id
              guid
              type
              originalTitle: title
              title: presentationTitle
              subtitle: presentationSubtitle
              description: presentationDescription
              thumbnail: presentationArt {
                url
              }
            }
        """
        variables = {"limit": 200, "seriesGuid": serie_guid}
        data = {"query": query, "variables": variables}
        response = requests.post(self.api_url, json=data)
        if response.status_code == 200:
            videos = []
            for v in response.json()["data"]["series"]["episodes"]["nodes"]:
                videos.append(Video(v))
            return videos
        return None

    def get_playback(self, guid, client_id, access_token):
        query = """query  {
          playback(
            guid: "%s"
            format: ["application/dash+xml"]
            platform: play_web
          ) {
            subtitles {
              useAsDefault
            }
            progress {
              position
            }
            pid
            smil(clientId: "%s") {
              video {
                src
                type
              }
              securityLicense {
                url
                token
              }
            }
          }
        }""" % ( guid, client_id )
        headers = self.__get_headers(access_token)
        response = requests.post(self.api_url, json={"query": query }, headers=headers)
        if response.status_code == 200:
            return PlayBack(response.json()["data"])
        return None




