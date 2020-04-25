import requests
import json
from pprint import pprint


class GetMicrosoftLearnInfo:
    """This class gives methods for working with Microsoft API"""
    @staticmethod
    def save_info(catalog, info_label):
        with open(f"{info_label}.json", 'w') as res_file:
            json.dump(catalog[info_label], res_file, indent=3)

    def main(self):
        """Main method, that does all job"""

        # main GET request
        response = requests.get("https://docs.microsoft.com/api/learn/catalog/")

        with open("tmp_files/catalogs.json", 'w') as res_file:
            catalogs= json.loads(response.text)
            json.dump(catalogs, res_file, indent=3)

        # Just in case, save products and roles in two json files
        self.save_info(catalogs, "products")
        self.save_info(catalogs, "roles")

        ids_links = {}
        for course in catalogs["modules"]:
            ids_links[course["uid"]] = course["url"]


        result = {}
        for course in catalogs["learningPaths"]:
            # Save course info from given API json
            course_name = course["title"]
            result[course_name] = {"url": course["url"]}
            result[course_name]["modules"] = {}
            for module in course["modules"]:
                result[course_name]["modules"][module] = ids_links.get(module)
            result[course_name]["course_duration"] = str(course["duration_in_minutes"]) + " minutes"
            result[course_name]["short_description"] = course["summary"]
            result[course_name]["long_description"] = ""
            result[course_name]["roles_and_products"] = {
                "products": course["products"],
                "roles": course["roles"]
            }
            result[course_name]["image"] = course["icon_url"]
            result[course_name]["price"] = "FREE"
            result[course_name]["uid"] = course["uid"]
            result[course_name]["number_of_students"] = "unknown"

        json.dump(result, open("mlearn_results.json", 'w'), indent=3)


if __name__ == '__main__':
    getter = GetMicrosoftLearnInfo()
    getter.main()
