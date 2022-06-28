# abtnetworks.com
#
import json
import os
import time

import requests
from SoarAction import SoarAction
from SoarUtils import output_handler

LogFile = "cve.log"
APP_NAME = "cve"
ACTION_LIST = ["cve_list"]

class CveApp(SoarAction):

    def __init__(self, app_name, action_list, input_data, action_select):
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LogFile)
        super(CveApp, self).__init__(app_name, log_path, action_list, input_data, action_select)

    def sendrequest(self, requesturl, sendjson):
        headers = {
        }
        self.logger.info("Url为:" + str(requesturl))
        self.logger.info("调用接口参数为:" + str(sendjson))
        data = {}
        try:
            resp = requests.get(requesturl, headers=headers, params=sendjson, verify=False)
            self.logger.info("status_code:" + str(resp.status_code))
            if resp.status_code == 200:
                return json.loads(resp.text)
        except ValueError:
            if len(resp):
                self.get_error_response("API请求失败" + "；Response: {}".format(resp))
            else:
                self.get_error_response("云端无响应")
        except Exception as e:
            self.get_error_response("请求数据异常:{}".format(e))
        return data

    def getsendparams(self):
        keyword = self.params["keyword"]
        page = int(self.params["page"])
        senddata = {
            'q': keyword,
            'page': page,
            'sort': ''
        }
        return senddata

    @output_handler
    def cve_list(self):
        requesturl = 'https://www.tenable.com/cve/api/v1/search'
        senddata = self.getsendparams()
        try:
            resp = self.sendrequest(requesturl, senddata)
            self.logger.info("调用成功")
            return self.get_response_json(resp.get("data"))
        except Exception as e:
            print('error', e)
            return self.get_error_response('cve_list fail')

if __name__ == '__main__':
    input_data = None
    action_name = None
    #input_data = "ewogICJsYW5ndWFnZVR5cGUiOiAiUFlUSE9OMyIsCiAgInBsYXlCb29rVmVyc2lvbiI6ICIxLjAuMCIsCiAgImFwcElkIjogImZlZDg5ZWEzNGFlZDQ1NzhhNTY3MTZjMDJhOTMyOGRlIiwKICAiYXBwVmVyc2lvbiI6ICIxLjAuMCIsCiAgImFwcE5hbWUiOiAiY3ZlIiwKICAiYXBwQWxpYXMiOiAiY3Zl5ryP5rSe5bqTIiwKICAiZGVzY3JpcHRpb24iOiAi5p+l6K+i5a6J5YWo5ryP5rSe5bqT5YyF5ous5ryP5rSe5o+P6L+w44CB5Lil6YeN5oCn562J5L+h5oGvIiwKICAiYnJpZWYiOiAiQ1ZFIOaYr+WbvemZheiRl+WQjeeahOWuieWFqOa8j+a0nuW6k++8jOS5n+aYr+WvueW3suefpea8j+a0nuWSjOWuieWFqOe8uumZt+eahOagh+WHhuWMluWQjeensOeahOWIl+ihqO+8jOWug+aYr+S4gOS4queUseS8geS4mueVjOOAgeaUv+W6nOeVjOWSjOWtpuacr+eVjOe7vOWQiOWPguS4jueahOWbvemZheaAp+e7hOe7h++8jOmHh+WPluS4gOenjemdnuebiOWIqeeahOe7hOe7h+W9ouW8j++8jOWFtuS9v+WRveaYr+S4uuS6huiDveabtOWKoOW/q+mAn+iAjOacieaViOWcsOmJtOWIq+OAgeWPkeeOsOWSjOS/ruWkjei9r+S7tuS6p+WTgeeahOWuieWFqOa8j+a0nuOAgiIsCiAgInRhZ3MiOiBbCiAgICAiSFRUUCIKICBdLAogICJjYXRlZ29yaWVzIjogewogICAgIm5hbWUiOiAi5ryP5rSe5omr5o+PIiwKICAgICJwYXJlbnQiOiAi6buY6K6k5YiG57G7IgogIH0sCiAgImNvbnRhY3RJbmZvIjogewogICAgIm5hbWUiOiAiQUJUIOWuieWNmumAmiIsCiAgICAidXJsIjogImh0dHA6Ly93d3cuYWJ0bmV0d29ya3MuY29tL3dlbGNvbWUuaHRtbCIsCiAgICAiZW1haWwiOiAiWFhYQHNhcGxpbmcuY29tLmNuIiwKICAgICJwaG9uZSI6ICJYWFhYWCIsCiAgICAiZGVzY3JpcHRpb24iOiAiWFhYWFhYWFhYWFhYIgogIH0sCiAgImxpY2Vuc2VJbmZvIjogewogICAgIm5hbWUiOiAi5o6I5p2D5L+h5oGvIiwKICAgICJ1cmwiOiAiaHR0cHM6Ly9YWFhYWC9MSUNFTlNFLm1kIgogIH0sCiAgImluc3RhbmNlRW5hYmxlZCI6IHRydWUsCiAgInNldHRpbmciOiB7CiAgICAicGFyYW1ldGVycyI6IG51bGwKICB9LAogICJyZXR1cm5TZXR0aW5nIjogewogICAgImNvbW1vbkZpZWxkcyI6IG51bGwKICB9LAogICJhY3Rpb25zIjogWwogICAgewogICAgICAibmFtZSI6ICJjdmVfbGlzdCIsCiAgICAgICJhbGlhcyI6ICJjdmXmn6Xor6IiLAogICAgICAiZGVzY3JpcHRpb24iOiAi5p+l6K+iY3Zl55qE5o+P6L+w44CB5Lil6YeN5oCn562J5L+h5oGvIiwKICAgICAgInBhcmFtZXRlcnMiOiBbCiAgICAgICAgewogICAgICAgICAgIm5hbWUiOiAicGFnZSIsCiAgICAgICAgICAiZGVzY3JpcHRpb24iOiAi5YiG6aG16aG15pWwIiwKICAgICAgICAgICJleGFtcGxlIjogMSwKICAgICAgICAgICJ2YWx1ZSI6ICIiLAogICAgICAgICAgImRlZmF1bHRWYWx1ZSI6IDEsCiAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgInNjaGVtYSI6IHsKICAgICAgICAgICAgInR5cGUiOiAiSU5URUdFUiIKICAgICAgICAgIH0sCiAgICAgICAgICAidWkiOiB7CiAgICAgICAgICAgICJ0eXBlIjogInRleHQiLAogICAgICAgICAgICAidWlOYW1lIjogIuWIhumhtemhteaVsCIKICAgICAgICAgIH0KICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgICJuYW1lIjogImtleXdvcmQiLAogICAgICAgICAgImRlc2NyaXB0aW9uIjogIuWFs+mUruWtlyIsCiAgICAgICAgICAiZXhhbXBsZSI6ICJzb2xhciIsCiAgICAgICAgICAidmFsdWUiOiAiIiwKICAgICAgICAgICJkZWZhdWx0VmFsdWUiOiAic29sYXIiLAogICAgICAgICAgInJlcXVpcmVkIjogdHJ1ZSwKICAgICAgICAgICJzY2hlbWEiOiB7CiAgICAgICAgICAgICJ0eXBlIjogIlNUUklORyIKICAgICAgICAgIH0sCiAgICAgICAgICAidWkiOiB7CiAgICAgICAgICAgICJ0eXBlIjogInRleHQiLAogICAgICAgICAgICAidWlOYW1lIjogIuWFs+mUruWtlyIKICAgICAgICAgIH0KICAgICAgICB9CiAgICAgIF0sCiAgICAgICJyZXR1cm5zIjogewogICAgICAgICJzY2hlbWEiOiB7CiAgICAgICAgICAidHlwZSI6ICJKU09OX09CSkVDVCIKICAgICAgICB9LAogICAgICAgICJleGFtcGxlIjogIntcInRvdGFsXCI6MjI1NCxcIm1heF9zY29yZVwiOjEzLjAyMzI3MixcImhpdHNcIjpbe1wiX2luZGV4XCI6XCJudmRfY3ZlXzE2NTUxOTMyMTFcIixcIl90eXBlXCI6XCJfZG9jXCIsXCJfaWRcIjpcIkNWRS0yMDE5LTEyNjYxXCIsXCJfc2NvcmVcIjoxMy4wMjMyNzIsXCJfc291cmNlXCI6e1wiY3ZlXCI6e1wiZGVzY3JpcHRpb25cIjp7XCJkZXNjcmlwdGlvbl9kYXRhXCI6W3tcImxhbmdcIjpcImVuXCIsXCJ2YWx1ZVwiOlwiQSB2dWxuZXJhYmlsaXR5IGluIGEgVmlydHVhbGl6YXRpb24gTWFuYWdlciAoVk1BTikgcmVsYXRlZCBDTEkgY29tbWFuZCBvZiBDaXNjbyBJT1MgWEUgU29mdHdhcmUgY291bGQgYWxsb3cgYW4gYXV0aGVudGljYXRlZCwgbG9jYWwgYXR0YWNrZXIgdG8gZXhlY3V0ZSBhcmJpdHJhcnkgY29tbWFuZHMgb24gdGhlIHVuZGVybHlpbmcgTGludXggb3BlcmF0aW5nIHN5c3RlbSB3aXRoIGEgcHJpdmlsZWdlIGxldmVsIG9mIHJvb3QuIFRoZSB2dWxuZXJhYmlsaXR5IGlzIGR1ZSB0byBpbnN1ZmZpY2llbnQgdmFsaWRhdGlvbiBvZiBhcmd1bWVudHMgcGFzc2VkIHRvIGEgc3BlY2lmaWMgVk1BTiBDTEkgY29tbWFuZCBvbiB0aGUgYWZmZWN0ZWQgZGV2aWNlLiBBbiBhdHRhY2tlciB3aG8gaGFzIGFkbWluaXN0cmF0b3IgYWNjZXNzIHRvIGFuIGFmZmVjdGVkIGRldmljZSBjb3VsZCBleHBsb2l0IHRoaXMgdnVsbmVyYWJpbGl0eSBieSBpbmNsdWRpbmcgbWFsaWNpb3VzIGlucHV0IGFzIHRoZSBhcmd1bWVudCBvZiBhbiBhZmZlY3RlZCBjb21tYW5kLiBBIHN1Y2Nlc3NmdWwgZXhwbG9pdCBjb3VsZCBhbGxvdyB0aGUgYXR0YWNrZXIgdG8gZXhlY3V0ZSBhcmJpdHJhcnkgY29tbWFuZHMgb24gdGhlIGRldmljZSB3aXRoIHJvb3QgcHJpdmlsZWdlcywgd2hpY2ggbWF5IGxlYWQgdG8gY29tcGxldGUgc3lzdGVtIGNvbXByb21pc2UuXCJ9XX19LFwibGFzdE1vZGlmaWVkRGF0ZVwiOlwiMjAxOS0xMC0wOVQyMzo0NVpcIixcImltcGFjdFwiOntcImJhc2VNZXRyaWNWMlwiOntcInNldmVyaXR5XCI6XCJISUdIXCIsXCJleHBsb2l0YWJpbGl0eVNjb3JlXCI6XCIzLjlcIixcIm9idGFpbkFsbFByaXZpbGVnZVwiOmZhbHNlLFwidXNlckludGVyYWN0aW9uUmVxdWlyZWRcIjpmYWxzZSxcIm9idGFpbk90aGVyUHJpdmlsZWdlXCI6ZmFsc2UsXCJjdnNzVjJcIjp7XCJhY2Nlc3NDb21wbGV4aXR5XCI6XCJMT1dcIixcImNvbmZpZGVudGlhbGl0eUltcGFjdFwiOlwiQ09NUExFVEVcIixcImF2YWlsYWJpbGl0eUltcGFjdFwiOlwiQ09NUExFVEVcIixcImludGVncml0eUltcGFjdFwiOlwiQ09NUExFVEVcIixcImJhc2VTY29yZVwiOlwiNy4yXCIsXCJ2ZWN0b3JTdHJpbmdcIjpcIkFWOkwvQUM6TC9BdTpOL0M6Qy9JOkMvQTpDXCIsXCJ2ZXJzaW9uXCI6XCIyLjBcIixcImFjY2Vzc1ZlY3RvclwiOlwiTE9DQUxcIixcImF1dGhlbnRpY2F0aW9uXCI6XCJOT05FXCJ9LFwiaW1wYWN0U2NvcmVcIjoxMCxcImFjSW5zdWZJbmZvXCI6ZmFsc2UsXCJvYnRhaW5Vc2VyUHJpdmlsZWdlXCI6ZmFsc2V9LFwiYmFzZU1ldHJpY1YzXCI6e1wiZXhwbG9pdGFiaWxpdHlTY29yZVwiOlwiMC44XCIsXCJjdnNzVjNcIjp7XCJiYXNlU2V2ZXJpdHlcIjpcIk1FRElVTVwiLFwiY29uZmlkZW50aWFsaXR5SW1wYWN0XCI6XCJISUdIXCIsXCJhdHRhY2tDb21wbGV4aXR5XCI6XCJMT1dcIixcInNjb3BlXCI6XCJVTkNIQU5HRURcIixcImF0dGFja1ZlY3RvclwiOlwiTE9DQUxcIixcImF2YWlsYWJpbGl0eUltcGFjdFwiOlwiSElHSFwiLFwiaW50ZWdyaXR5SW1wYWN0XCI6XCJISUdIXCIsXCJwcml2aWxlZ2VzUmVxdWlyZWRcIjpcIkhJR0hcIixcImJhc2VTY29yZVwiOlwiNi43XCIsXCJ2ZWN0b3JTdHJpbmdcIjpcIkNWU1M6My4xL0FWOkwvQUM6TC9QUjpIL1VJOk4vUzpVL0M6SC9JOkgvQTpIXCIsXCJ2ZXJzaW9uXCI6XCIzLjFcIixcInVzZXJJbnRlcmFjdGlvblwiOlwiTk9ORVwifSxcImltcGFjdFNjb3JlXCI6XCI1LjlcIn19LFwicHVibGlzaGVkRGF0ZVwiOlwiMjAxOS0wOS0yNVQyMToxNVpcIixcInB1YmxpY19kaXNwbGF5XCI6XCJDVkUtMjAxOS0xMjY2MVwiLFwiY3Zzc1YyU2V2ZXJpdHlcIjpcIkhJR0hcIixcImN2c3NWM1NldmVyaXR5XCI6XCJNRURJVU1cIixcInNldmVyaXR5XCI6XCJNRURJVU1cIixcInRvdGFsQ1BFXCI6MH19XX0iLAogICAgICAgICJkZXNjcmlwdGlvbiI6ICJjdmUgc2NhbiByZXN1bHQiLAogICAgICAgICJmaWVsZENvbW1lbnRzIjogWwogICAgICAgICAgewogICAgICAgICAgICAibmFtZSI6ICJwdWJsaWNfZGlzcGxheSIsCiAgICAgICAgICAgICJ2YWx1ZSI6ICJJRCIKICAgICAgICAgIH0sCiAgICAgICAgICB7CiAgICAgICAgICAgICJuYW1lIjogImRlc2NyaXB0aW9uIiwKICAgICAgICAgICAgInZhbHVlIjogIuaPj+i/sCIKICAgICAgICAgIH0sCiAgICAgICAgICB7CiAgICAgICAgICAgICJuYW1lIjogInNldmVyaXR5IiwKICAgICAgICAgICAgInZhbHVlIjogIuS4pemHjeaApyIKICAgICAgICAgIH0sCiAgICAgICAgICB7CiAgICAgICAgICAgICJuYW1lIjogInB1Ymxpc2hlZERhdGUiLAogICAgICAgICAgICAidmFsdWUiOiAi5Y+R5biD5pel5pyfIgogICAgICAgICAgfQogICAgICAgIF0sCiAgICAgICAgInZpZXdzIjogWwogICAgICAgICAgewogICAgICAgICAgICAidHlwZSI6ICJGT1JNIiwKICAgICAgICAgICAgImRhdGFTb3VyY2UiOiAiJHt7ZGF0YX19IiwKICAgICAgICAgICAgInN1YmplY3QiOiAi5Z+656GA5L+h5oGvIiwKICAgICAgICAgICAgInRhYmxlIjogewogICAgICAgICAgICAgICJkaXJlY3Rpb24iOiAiVmVydGljYWwiLAogICAgICAgICAgICAgICJjb2x1bW5zIjogWwogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAidGl0bGUiOiAi5oC76K6w5b2V5pWwIiwKICAgICAgICAgICAgICAgICAgInZhbHVlIjogewogICAgICAgICAgICAgICAgICAgICJzeW50YXgiOiAiJHt7dG90YWx9fSIKICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgIF0KICAgICAgICAgICAgfQogICAgICAgICAgfSwKICAgICAgICAgIHsKICAgICAgICAgICAgInR5cGUiOiAiVEFCTEUiLAogICAgICAgICAgICAiZGF0YVNvdXJjZSI6ICIke3tkYXRhLmhpdHN9fSIsCiAgICAgICAgICAgICJzdWJqZWN0IjogIuafpeivouiusOW9lSIsCiAgICAgICAgICAgICJ0YWJsZSI6IHsKICAgICAgICAgICAgICAiY29sdW1ucyI6IFsKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgInRpdGxlIjogIklEIiwKICAgICAgICAgICAgICAgICAgInZhbHVlIjogewogICAgICAgICAgICAgICAgICAgICJzeW50YXgiOiAiJHt7X3NvdXJjZS5wdWJsaWNfZGlzcGxheX19IgogICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAidGl0bGUiOiAi5o+P6L+wIiwKICAgICAgICAgICAgICAgICAgInZhbHVlIjogewogICAgICAgICAgICAgICAgICAgICJzeW50YXgiOiAiJHt7X3NvdXJjZS5jdmUuZGVzY3JpcHRpb24uZGVzY3JpcHRpb25fZGF0YVswXS52YWx1ZX19IgogICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAidGl0bGUiOiAi5Lil6YeN5oCnIiwKICAgICAgICAgICAgICAgICAgInZhbHVlIjogewogICAgICAgICAgICAgICAgICAgICJzeW50YXgiOiAiJHt7X3NvdXJjZS5zZXZlcml0eX19IgogICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAidGl0bGUiOiAi5Y+R5biD5pel5pyfIiwKICAgICAgICAgICAgICAgICAgInZhbHVlIjogewogICAgICAgICAgICAgICAgICAgICJzeW50YXgiOiAiJHt7X3NvdXJjZS5wdWJsaXNoZWREYXRlfX0iCiAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICBdCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJ1aUNzcyI6IHsKICAgICAgICAgICAgICAibGluZUhlaWdodCI6ICIyNnB4IgogICAgICAgICAgICB9CiAgICAgICAgICB9CiAgICAgICAgXQogICAgICB9CiAgICB9CiAgXSwKICAiaW1hZ2UiOiB7CiAgICAic21hbGxJY29uIjogbnVsbCwKICAgICJsYXJnZUltYWdlIjogImRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBTndBQUFCNENBWUFBQUNaMTV4NUFBQUFBWE5TUjBJQXJzNGM2UUFBQUVSbFdFbG1UVTBBS2dBQUFBZ0FBWWRwQUFRQUFBQUJBQUFBR2dBQUFBQUFBNkFCQUFNQUFBQUJBQUVBQUtBQ0FBUUFBQUFCQUFBQTNLQURBQVFBQUFBQkFBQUFlQUFBQUFEdnhZc3pBQUFXdzBsRVFWUjRBZTFkRFpRY3hYR2VudDI5T3lGK2pNRUlUaitBSklPQmdIRndiQ3dnenp6SHh1L0pHSkNSRURaZ1pBbUVqQ0liekFQODh1TzhtTmc0T0RFL3RoN0UvTnRTUU9Jbmlnd0pmaEJoNXprRWdnbGdFWkE0ME44aEljeVBKSVIwdDdzem5mcXF1MlpuNS9idVZzZmRhVTZ1RnJOVjAxMWRYZjExVlhkUDc5d1NCSm9VQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRWNnbkFpYWZaZzJlVlhiRllXMUJ0OTAvaU1vdGc2ZTFGMDF4b1dwTzczeE5TdTNUSjVTQ3pSdmI1VDZoWTlvM21vLy90aUwzOXVHeDR3SWJGK1ErMkcvZnQ4M0pxOTVON29lUXNTdmFEd3gyMk5GRDJNVFFxRzRadGNWODl0V3RRNk44NkxRV2gwNzE4R3EyS3o1ZERONTc2WlE0Q0Q4UnhORkhBMk9PSndzT2o5N2QyZGFiSlpZS01PT0FJZ21mekVLR09FdWxvRWpDZ3paSXh0ajFsSDFvVXJUcDlhT2pJSDQyYWNBWEZGN3ZQSmJZbFNJWFY2dFBrc1lrTU0wN1crZFQyVStrZkNobzlJdURyNkQrWEJKdGp5YXhmblJKQUdqVW9KUjVLTGhQa3RkUW5nb0ZyMGJsVXRZTGx0a3FhZk5NWU40cWxIZWVRREljY1BhaE1aK3N4bVphc1JBOFhxM1lLYVV6TnY5VmRkbVlmeXA4OGZXNWhnWWxxMnQzM28vb2dNUHFGVzN2K2tJUTJ6T2piUzlPSlkvNWdBMGk4aHNNdHNBcUhrTDM0aUErUzBxRVdocDhHaUR5RTFjWlF3VXVHVElFWG93TVh5UHJOSkl2VFlOYTBRNy9jL3BUeHJFazFIQTd2bTFqd3JTR1FlWEpCaFAvNnlGMzJqaTR3RGRhMHc4amZCSmJCWXNFVHkvRE9NWFNINnFVd1lMcmMzWktxU2duMmw5OXhsaDBRdDdYSldTaU1BeG5tcWtiMTRrNk0zWHprOVhsWXc0TDdLai9EWUt1VSsxRFk0K0lxbEZaeXZORVIyVEEyV1ZIN2hNSDc4Nkx0M1ZkVG80d1JvYURuWmFHcHZFUWt4UVZzSXdYWUo1R3c5OVNUUVFidExuaGRlVXBmU0xvYVE5NUJHTW1rV043YlVRUmtKQUo2M2UzeVFRaGJVY1pKWU40Ry85aTdGWFV6QVZzRndMYzJ3elRVdjd0TUJCN0dyVXZaVVJkZ2dKd0RqdjNLWGRlSkVXeTdiTmtwajdORFFsMk5kdkNiNXN2Ykh3MHBhcWVMWVMvcEdCYkVJVDJQK3NMOG5FM29nTE92bkJNUy96eVcxZkg5dDF2MGd5NlA4YUhuVDRWTXRhRkZLT2JkYUllc3paSkpmN2lhdmdjN3pRZ0pBQTlTTm42MUhaTVB2Rzh1SVcxOFZ0MldmdkhuRFJOeFpFOXdsaXpqbVRlY1FwOFNSanNGQmxRRzRjclNlWU5adzAzOW1hNmZMQjR1MnpzcVhFVVgrUENnRHBHamJvMllRT3hkQ3NCeUo3dUFPYm1SWkt0UXkyUEMyZ2pBUm1YR2phWjNZTnZTN0JOYlBJaDVsWklUSURTQUxleXBIREd4dXQ4aTNXa2VQcm1lMzNHNjBSOVFJcTFkYUs3OVNaL0Z2VUNoMTAyYm5JMWp1NmhBTURlblJPTVQvbEV3c3NROVN5blFhZC9MaWd4eEk1UG5JTDBTUjNYZ21odnJKRmt0eGVuYmRySHlaSXR5OXNuMERQRU9ybUhycUFRbkZjOFk5TWl5V3VHV2p1OVlNelNRVjNuN0xMeDdWRmNvUzJYT1FnMjlKZzh5UE1scjVHTndFendRcm53Q1hZVUdPbnRlS010b2FDSit0S1dCSlRVNVYxQWcvTFFtSlhoWGg4NjBaejIvSHVvUDFMVGlGamhxZytPT3krSzRvVTA1dVRjdFpDUU1CQ0tRV2pFMS9KQ0gyenVHY2tGbnVTNUlheko0aDV5eUpGbkt1R2RsRGdiSkNYUml1YmJjRFhwdmw2bENBNGp4V2xwdEdIVFV0cWlIY1NUQUxkTkhGdm1jdHhDZ3FCcmJKZ0xNQmRva0lDWTVPR2VlY29VVEtCSDhsQXVhb1dpVk5ya2NpNlFQT1FJVDFxTTJVTFBiV2VOOUdCRHIzSWZjTkY5N2ZOcEczUVRqT1ZCaEovNFVjdk9pcENwVHhDRVE5V0d1YjQ4ZXlleXpnbGRQY21EclBDdVBCWkRFalZ0UVJ6djVKayt5WW9rV0pPY1lXZXE2emY5a0E2V3BzRDh4R1RoWFZlb2lCeWMvaVVCNDNuWkRRaUNRdEdKUm55U1IweHF4NXFGam1xallVaDdBeEkrMFVCbFhFb0h6K0ZYekJtZEhad3h3ajl5SFhDVis4YWZabTEwdlF3S0R3Mk5vZ3dSeG9qdi9CaGxBNUsySVJFZHBHMHdvWG5ialpQVWRKUWYzRU55TkRrNG9OaXdNV2xNWWdRTWxFdUc4TDdCd095b0cvOHdMdE1rOEl6a3NkNWk0TnVXM0dib01kVEEwbVlFKzVXcDN0OStEdG14Z0RFVXMxRkxlRTlkWUxtZ2MwcUZGOHdnQ0Y0cUNpL2xybGJkcDRnaVUzaWhuQ0U2SUNCOHZUN0M4enVGTXpzZmhzU2VrT3A3bDZNZTJTVVRqcTdhNmhPMFhPd3IrL3lzZVkxV09EeUswT0Q5TzhuZVdyQXRqNWtaUS92bGFIWHAySDhtWC9sODFqYjRsYmdReW9RSHBaRCtRZUhzem11UlA1VEpQbkRvVWRXbzhoVFpzbmU2ZmJUWnAzM0dyQ0NSbXd1dHJmOGRtT3F3ZkFIZkt3NVQxMjJoY1lhNWUwVENPT1F1MlNYVEMxWDdYNzhqbEk4U1I0R1J3b3ZSMlJXTlZxWW5pbkV3ejh4ODdibmg2cFI5WU5KQlVkVDlISjFRSHB3Y0ZQVFRPQVZjcFJDR1U4elpHNTd1UjNUQXhYYkZNWHRYZi8vT1UyVFRVYXdrQTFhUGdQT0hKclFyV0ZnNGU4cUN3VDYwR1hCSDlyQ0tzbGZLVmJlaTZJa0xhUnQwRkI5QTBIWVBOTTFqcThiYk5RcEJvVFFML3FBNHZmT2s0UXcyZ0dhbXZmS0dEZVB6eWNMWTB2N1ZUUXRrRjgvSmpqS1B3eFRrT1ZxcVJQRWkrOGh4US9aS1ZlWE5MYmRSVzBjSlZtaWJlVkM2R0U5UEJkdlFoZy9UeWp0Zmd3MGpPelFwbHdGSGZuc1ZPeWFlcmVDZ0VtQ2VSeDR1M21nUUxaamdxdEk1blZmdnJxMUg2VXNiSDdVMnZMWXZXM240WUxja0d4d1JiWHY3UjNJN21EUmFPdmFiSmc1bVFDZGE1RmFCRnpKZ2c5Z2hsUE9EdFlYUjRYbTdDME9ZOEllUWVBenkxTkh5b2drbjBHTGh0bG8wQTdPWGdDTEJXc25EUFdab1kvNmw5T1VOWitGMmR5YTh5MW5kM1BFck9ueVlBanZnM25XbmZyU3NrSzIwdWtobm5MV2hDYzhzenR5d2JMQnNyOXc3NFNRNktsMUJiWmZxZERiQVR2QWt1N3FMWVhpU21iSCt0M1YxOUdiUUVjamRDa2YrK0VXWmhkazNhUllHWlI0ckhmd1ZLeDlkdEJYYVVXd2JQV2ZRVVJtQVFuUHE0OVZpMkhLdWljMDdzSTIzbDU3S1ZsT29temtRQVJ5QXQ5cjdEejFrQUUzMnFHSVhIejZHanYrWEVFUWx0NHBSRzM1Rnc3WVJQR2lhNTd3Z21LL0IxZ1BPSWNuSVhjQ1JRY2ZMRmhLT0FWNmNoTit0UTU1Y0pyalhUSHZwclNGQlpnQks2VVIwUFMxaXN6bWd5TWFFZ3NkRWtWRGlxVi9Jby80ZFdPMk83NkNWRHhVR25QaWd5VlR1b2FCdVo5M1FoRFo4QW81SWdxM3daT01keFptZHQzS2hmZ3c1QXJuN0hvNVdzRC9pR1ppNkxsc3lVQ1I0SkRqeFRCTVU3NlRiWEtYaXVaMFBsaGVOcHordHNaZnlaQ0hHdWk2NERyREZWTURMTmEvZ3AxVVdIMHJmbFFVM0RMUXo5QmMrMzZPWS9iVFQ2YlZJbTVuMmNJdlZsdjRxNGRsU01iN1VTOWNSKy9EQkg0cWk0QUdXcFE5MFE5UUpMMTJycTlqVVRWYURqS3EwMEZnSnJjMlBGRTdmZEUzajBwR1JtN3VBbzFIZG4vMlE4U05uOUxRUm5NVnE2d3VOOG5kM1hxbTljRVhsdGVoa2NxdVBKbDdhdzZpTWs5bmdXbnZQK01mTXpBM0ozOG4xcU5KTFJuWHhZV2ZHY1hTbEsvWmhJTDdyS1o0ZDA4K1E5T3k0cFZpd1o1c1puWFV2VXRlYUtMVGFLRG9aOTdScWN4eURTa3F4a3BWUWpKL1VjWm4xZlhWbHNNZVhzbTFvd3hrcmRvSktJdmJWc0tXd1VPNUhLczNkbHBLMlFXM3NwTUErYy9GNFVKNGZsKzNtcS9uWlRxWWR3Snk2dHF0a2krZVEvZS9CVnI1b1M1ZFEzazY2N2JJOFkxSDl0a28xV0d3Zm50eWExdFVmYjVkTW1oekg4WjNBaW5ISllKWmdpRFVLWlVUSmthMEpDeGRRY0wvU2wvNWtLMC8yZ3BmdHFLWFhxcGtIYlhDeExPVkwvY0NHL3JtUjNJMzRnTjdtU1NqZTdQRjVvTGlnVXloNGt0MFIydUpaNXZPZEEzaHJwNjhlRG45Wi9nSU9ML3Z5c3c0R3BmZUx0azliaHgrdTVsczA1NjlaRlpyQ3BlTHc1RmJVSDNaM3VEd0hoOUJVVUI1YmViUGM5QnNvZHZrSmUxVzZxdmZUSkxVZmRMQ2pFMDMwcFhncGMwRVFmci80NVRYTCsrd05yWHNTWUVGTVFZQkpnaWhmR0Jmd3ZZd1B5MUpacmI3VHhjK1VtSGhZVjAyL3lBbEZNTElNQWhGWEhNeW1keW1mNzlQZUVWSkl2Y2xYSWgvWlhBUGVEdzVsaXVNS3BiQThHQWNGK2JLKzNwcmllV3Z2TWtHNHlEazdiYUhnaEJRTnZIWHl2RGl0QzBqNk5NRTNLajg3L0xQMW1ocmZWZDU1ODJiU2RSd0hXeXFJRTEwYzVESnBrUTVxay83OVI3SDFFMy9kV0dOOUx0NHJ4WVZBRWVxQ3h1WHhTcFhJT0ZrbkovVWc1OXNYU2piVTViRituNWZ3WkFmenNEbjhZWEhheG52cUxSdTVkN2tMT0FMNmRYWUxPQkFOTlBoR0FVaDVoV0Q3TThudmdPUjFDRXI3dGMyamdIaVpBcyt2YXJSdHdzdlFOSWtJQlk4K2dzYjBDeEcwUmJ6TDN2V1JBL3JxVS9udXd5NGhoZWZMQkNUMUcySEYrakZwQmNGcnhiYlNURE9qdWIrMWM2dWhId2RNRUJ4NHBJV0NnZHZ6QVFJNTVEVXJMM1VUZlY2M1RENGN0RTdubzhYNFUxZXo1WHZJUis0T1RXallWdEtzL1NuZ2kyQ0RzekNsZXd3UW5xTjV3T2krRWdhZklYSW5YYmxONW94Vjc1Wi9kdWhNK3FtVko2Z3ZMYnk2c2JYa3RGaWEwRWRPd2hPMTlwQ3k2Zm9wWlUvemhYV2svUE9KZnhKVTR4dTRlbEsvVG9SdVV2cm9qazRrSzlUaWRET2o0L2RaeWNiM28raFpxb3VMK0JDRHNYZTJ3bTc4N2txdEw4RTZrbG5EVGFJdDJFVE55N2dsUEV4cXFweUViTENqMkxMM0JXWmFjNU1ES3g0Qkg3a0xPTnF5UEVuamVWRnYyRGtuYzZXMEVueU51RHQ3azgxTGZzdjU2NTRwMzNIWWxlU2cxeWRPQ04vRkxPNTh1TVlqRDhuYXM4cTNIejZuNVd0cjZyNGp3OHBYcm5UZFJ3SXQ5ZlhoNFZRM0FRaDZKT2lnTVA1VzZjTDFUNEJyT21IVnBlVGpKRVdkalJSMlhFNHZQUCs4ZE82R3YrUWIvZWdUZ2R4dEtVdkYxc2ZJS1RHZitoblNVZWVvdFR6MjFEZzRwWEw3eEQvcnM0YzVLV3ladGZZR1doV1dzOWVTQi9NcTdhbXMyRUtkeWVUTUpyN2Uzakh4dzlJRmEvOG03SzUyTGFidjBDYndjeFVpQVVIQmdVSHlRaEVJSENXTzBsYnZucFpaNi9tUGVFVlh2eFJmRmlENEcxeThoYVI4MlVMeUFVcS9DbFVBQ09RdTRNeXNsOWJTSVA4Yk81UjNKamdpTzJPS091ZWlIK3FwMkx2c0xVY2NPQktHc3lWc20wV1FkemFhVE5BL1RDZEpYeWxnNkhsdWRDV083N1YzVDV4QXE2TXAzM0gzOTJrRisxdzZtSGppOGZYQVMzMHNkSXhaRVB4ZnFiVHZuSUhnZzJjcHZuRDBEeDYwd1NWak1aQTIvdERxNUM3Z01BQ2hOVDltUjByTjBtNWw4RE8zekxvY2tLYTliS3VQMjlzbmpjLzc0T0Y3dzlBR1g2RytSQklRVEttZkhHeWVTdUNCeG5Id3NYSjMvR0w1dHNOZnMxRjhKZkx3RDNnSWJZUU5TOWx3ZTB2WStpVnp3Y0IrZUlmZUM2VkYxcTF5UWh1dGVHU2pwaVlSeUdYQUZlZDJQRUtuWGgwWVhKNmxmWUR4UXpyeXlFdnIrRGc0cHJ2TFB0Vjk4OFJ6bSt6M2JoTXJ6Vm56YXdMOWI3RXFrQ3NuVzBMdUorWEpDb1VpdjBJaG52WWlMTndMem9JRm5OemprOGlsSEIrQlRQdVgyV2JXNnBlZ2F5QXBzWVZYT3RLQTRFdnh0ZkpjdXRGQXVqemtkWEtKRk42RW9KWGd1K3cwNURpeUNyQ0R3Wkc4MDJYb3diVGRXZHo5azBuL1UxNDQ2ZUwranRXSEhOaytHaWpPdnZBYU91QjRuTzNuc09QMWlHbzRpaytVQ1FYUGYybmdxZU5KQkgvd3luZ0lKa0x4aFVONGZldnNOVXY2TUtQZklnbW9MRFgraTNCUVhKcWFSNEFuMmViRmgxZHk1OExKZDlQZlVaOFBuMEtDc2VERmFGcm4yQ2xCT1VtaHY2VWZEM3Fab25VdE9iZjdYUTZzQVBBUFdRbUU5ejdUVTMrdFRkYmZUMzJXcVgxc2FQMTZ4MldZUEdwWk5jN2VkbVI3ZDdYeUhFV05lLzZVRTBaUUpNd3lrb2Q3NFgxNW43WWE4NXRXdS8rcFptN3RmeGdDRmJ1UzdFOG5qeXNIMFFiVXdXNkMrc0VVOThLRCt2UjNyUmV0MFZOS1FhTVBtaURXaDh4dUs3SjNIemU2dkhYSDAvUnpkQjloSTdKZXRvdVdaYXRuNG5NWHRTRVl5UWw5MEtOeWlpL1RVZm1mdHN4LytjbStsSGJkTW5FcWFWZ09mKzRwTjBCcmpkbmNXaXo5c1ptOWFtTlBuYzNuSU9DNll4ZHdQSitKT1kxVVVCbjlWK3RGRmxpcEM5cE02cTgrZlVkbmlxV1RXbWF2ZnE0WmRYbVN5ZlYrZ0IvMmk2WHB0Q3pSVDMvVGFQSEs1Q2w0YkMyRnBubmtjWDZLMGlCaWF3VG5rUzBTWkRndmtkOVZmVkFHSFJScXZMM3pXNzhndUt5L1lDTkxncmE1cno1RWg0OC93bUxHZWp4MXZOZE5oZTU1bFVRZ21NaVFyY3lEWXZYaENTQ2luMDJmK1g2RERiWnhpa2czTG1BckZHMHhqbzQ2L09od2g5NlFzUkV0NTNRSnoyL05JTC9xODRneVgvVjVST01HRjUySWNqNW9taGZaSUM3TUhZbkJCa3h6SFhBd3NIWGVpeXRwYUU4a2oxb05sMkxINWdVQmpnQUpUOU44VWs1bFhBNlpGQy9sV1pyV0FSNTFFdXAxY0Y1amZXeWJDUmUxL1hsSDAzOUcwdnJCVWQrbTU2Mm4wWlo4djhXOHQ5czl5Ym4yMHM5ME5idGdwN2MxRHY1aTFMeU94K2x1Y0pMdnEzdGpuN0QzWHduQVR2RHlQUnlDanZQOEJNWnYrbk9lZS9zZjlpSFAyVm5qa2VmeTBYZVVlMXo5eWFnYzBxUXB5ZDNRT3E5ajBlQjBjUGkxNUQ3Z0FFbmJnbzVYMmthMzBldGU1bGYxVGxjZkJObVpGL2ZwQ3dQdVpFaHBpaGVaSGlzZW5KNTBVTHZ1RWg3VTZ4WUtIZlEzWml2Yld2ZTlHRFdhVFdiR0MyVWJtcG5rYk50NEFZTmRkTEZlVDlOOFdpYk5VOXZMV3VhOTh2Zk50dHVNWElJTEFneDlUZ0xDQndjT1RQamdCRGpoQUlWR3g1OWlDbVVkdERvbU5NMExoajZQVjlFVUwrMGpHTUhUejBYOXV2WG84VmMwWTN0ZVpVWkV3QUU4TStlRnQ5c09PZjR6ZFA1MktUbmFXN0tOUzFNRUkrNUI4Uys5VWlUT0lrNUROQzBESGc0c0ZEd0hwYWM4TzdOT3RnWVdPUWYwbE9wdG8xK09uMFlIRlRzZ3NTdXBiVzdISzlUNkpXNkZvNXBvTTlNVzIwcDU4Zzh5bk9kb1IwdTQzMWQ3TzZEWkZWc1NXYnhwZ3BXbXdjVXJPUWVXMjByVDFwRnhCOFdGT2tLNVBqQ0hIc0ZlZU5BMG41U1REcTREWGRETjk1MnRoVkhUOGRzeGREZGlFL1Y0NUNXNzhOajlkM1oxZlljY2JnNDkxNHlHYjNLQ280Sm5oM1ZaNlU4Y3FuRlFlWG5oT2JoUXRaL3l0Qzd3YWZtd1lLYTFmbVAxZzFtWlhibnYrdkhrZjZEK1hNNTFwQi9lMXNUd2pMRjBFcnVWRGhCT2FaMzcwdTkycGEzK1pPMk5rOGQxUllaUEtYdktab0d1TjFZT2owQWJKVXdVSW9OeTRVVStXMDdpM1lXUURxRVdySDZxa2I2UmxDZkRPWkpzVG15bG8vVjl1cmJaYzJnV25FVU9lU0t0YmRqclVMbnJWam9nVUNrYllEVlpjWXg2eCttdnZwU0hvYm11N2ZKVi9pY09Fdk1HeEhUZGRBVDlIa3I4ZFJ5UXlQRjdRMFZrS3YyM3RWQXNUaTNOVy9XYmhqTHZJOVBlZU55NG5aV2REUU91SHFXZUtHYWJsWDdJMXdqOTlpMmpnQ2FWaTBaZHRycnVKZTZNeUlpNUJYWjdSTEkzZm5MZjd1cVdLUlE2SDZjL2hXa25ienlBK015V0dYc1RaSUVpQ1o4UmM0WE5mcjR4YXNKeEM1cjlHN05tbE82ODZjT1lRSzRqMlFONGxrQWxpVzVRM0FiQkwxdkQwc1ZtL292ck9HT1FQK3cvSHZQQjdyaDZDOVJtVVh2L1RXVTE5ajRPMU4zblIzMXIxWGZmZjV2NTBMREhCRncrNEJ3OEsrd3RKK3hWN3Q1NkZybm1hUlJlUjlJTEFFVTZsWG1idGwxUEZRcG1hY3VsTHo4N2VLMnBKa1ZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlFCUlVBUlVBUVVBVVZBRVZBRUZBRkZRQkZRQkJRQlJVQVJVQVFVQVVWQUVWQUVGQUZGUUJGUUJCUUJSVUFSVUFRVUFVVkFFVkFFRkFGRlFCRlFCQlNCWVVQZy93RUFJVHpMUkVTOTFBQUFBQUJKUlU1RXJrSmdnZz09IgogIH0KfQ=="
    #action_name = "cve_list"
    app = CveApp(APP_NAME, ACTION_LIST, input_data, action_name)
    app.do_action()
