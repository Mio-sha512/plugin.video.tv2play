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
        response = requests.post(self.api_url, json=data, headers=headers)
        response_data = response.json()["data"]
        errors = response.json().get("errors", None)
        if errors:
            for e in errors:
                message = """
                    Message: %s - 
                    Type: %s -
                    Debug: %s
                """ % (e["message"], e["data"]["type"], e["data"]["debug"])
                LOG.error(message)
            return None
        if response.status_code == 200 and response_data != None:
            return response_data

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

    def get_structure_content(self, structure_id):
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
                url
              }
            }
        """
        data = self.__do_request(query, limit=9999, entitySort="popular", structureId=structure_id)
        if data != None:
            series = []
            videos = []
            for s in data["structure"]["entities"]["nodes"]:
                if s["type"] == "series":
                    series.append(Serie(s))
                elif s["type"] == "episode":
                    videos.append(Video(s))
            return videos, series
        return [],[]
    
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
              title
              subtitle: presentationSubtitle
              description: presentationDescription
              thumbnail: presentationArt {
                url
              }
            }
        """
        data = self.__do_request(query, limit=200, seriesGuid=serie_guid)
        if data != None:
            videos = []
            for v in data["series"]["episodes"]["nodes"]:
                videos.append(Video(v))
            return videos
        return None

    def get_playback(self, guid, client_id, access_token):
        query = """
        query GetPlayback(
            $guid: String!
            $clientId: String!
        ) {
          playback(
            guid: $guid
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
            smil(clientId: $clientId) {
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
        }
        """
        headers = self.__get_headers(access_token)
        data = self.__do_request(query, headers=headers, guid=guid, clientId=client_id)
        if data["playback"] != None:
            return PlayBack(data["playback"])
        return None




