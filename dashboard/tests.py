from datetime import date, timedelta
from json import loads

from django.test import Client, TestCase
from django.urls import reverse
from .models import Department, Teams, Users, Objectives, KeyResults

# Create your tests here.
class DashBoardTest(TestCase):
    def setUp(self):
        Department.objects.all().delete()
        self._create_model_data()
        client = Client()
        objectives_analysis = loads(client.get(reverse("departments")).content)
        self.objectives_analysis_status = objectives_analysis["status"]
        self.objectives_analysis_data =  objectives_analysis["data"]
        url = "%s?%s" % (reverse("teams"), "department_name=product")
        teams_analysis =  loads(client.get(url).content)
        self.teams_analysis_status = teams_analysis["status"]
        self.teams_analysis_data = teams_analysis["data"]

        
    def _create_model_data(self):
        usr1 = Users.objects.create(
            user_id=1,
            first_name="Navneet",
            last_name="Menon"
        )
        usr2 = Users.objects.create(
            user_id=2,
            first_name="Kailash",
            last_name="Raghav"
        )
        usr3 = Users.objects.create(
            user_id=3,
            first_name="Johnson",
            last_name="Stevenson"
        )
        objective1 = Objectives.objects.create(
            objective_id=1,
            objective_text="Improve HR Processes",
            user_id = usr1
        )
        objective2 = Objectives.objects.create(
            objective_id=2,
            objective_text="Raise participation in Surveys",
            user_id=usr2
        )
        objective3 = Objectives.objects.create(
            objective_id=3,
            objective_text="Improve Engineering Processes",
            user_id=usr2
        )

        key_results_set1 =((1,'Set up onboarding process','Pending', 
        '2020-08-11', '2020-08-04'),(2,'Conduct 3 Surveys','Complete', 
        '2020-08-11', '2020-08-03'),(3,'Implement organization chart',
        'Complete', '2020-08-11', '2020-07-27'))
        for key_result in key_results_set1:
            kr = KeyResults.objects.create(
                keyresult_id=key_result[0],
                keyresult_text=key_result[1],
                status=key_result[2],
                due_date=key_result[3],
                updated_date=key_result[4]
            )
            objective1.keyresults_set.add(kr)

        key_results_set2 =((4,'Draw up survey participation incentive plan',
        'Complete', '2020-08-11', '2020-07-25'),(5,
        'Create Survey non-participation list','Complete', '2020-08-11', 
        '2020-08-01'),(6,'Speak with survey vendor regarding employee complaints',
        'Complete', '2020-08-11', '2020-08-02'))
        for key_result in key_results_set2:
            kr = KeyResults.objects.create(
                keyresult_id=key_result[0],
                keyresult_text=key_result[1],
                status=key_result[2],
                due_date=key_result[3],
                updated_date=key_result[4]
            )
            objective2.keyresults_set.add(kr)

        team1 = Teams.objects.create(
            team_id=1,
            team_lead_id=usr3,
            average_pay="20000"
        )
        team2 = Teams.objects.create(
            team_id=2,
            team_lead_id=usr2,
            average_pay="30000"
        )
        team3 = Teams.objects.create(
            team_id=3,
            team_lead_id=usr1,
            average_pay="40000"
        )
        usr1.team_id = team1
        usr1.save()
        usr2.team_id = team2
        usr2.save()
        usr3.team_id = team1
        usr3.save()

        dept1 = Department.objects.create(
            department_id=1,
            name="Product",
            location="Bengaluru",
            date_of_innaugration="2019-07-1"
        )
        dept2 = Department.objects.create(
            department_id=2,
            name="Engineering",
            location="Redwood City",
            date_of_innaugration="2019-07-1"
        )
        dept3 = Department.objects.create(
            department_id=3,
            name="Marketing",
            location="New York",
            date_of_innaugration="2019-07-1"
        )
        team1.department_id = dept1
        team1.save()
        team2.department_id = dept2
        team2.save()
        team3.department_id = dept1
        team3.save()

    def test_analysis_status(self):
        self.assertEqual(self.objectives_analysis_status, "OK")

    def test_objectives_on_track(self):
        filter_date = (date.today() - timedelta(days=7)).strftime("%A %m/%d")
        self.assertDictEqual(self.objectives_analysis_data["objectives_on_track"],
                             {"date_since": filter_date, "on_track": 1, 
                             "total": 3,"on_track_ratio": 33})

    def test_objectives_updated_recently(self):
        self.assertDictEqual(self.objectives_analysis_data["objectives_updated_recently"],
                             {"date_since": "2 weeks", "update_ratio": 67, "change": 0,
                             "percentage_change": 0.0, "direction": "up"})

    def test_departments(self):
        self.assertListEqual(self.objectives_analysis_data["departments"],
                             [{"name": "Product", "teams_count": 2, "users_count": 2,
                               "objectives_count": 1, "objectives_on_track_ratio": 0}, 
                               {"name": "Engineering", "teams_count": 1, "users_count": 1,
                                "objectives_count": 2, "objectives_on_track_ratio": 50},
                               {"name": "Marketing", "teams_count": 0, "users_count": 0,
                                "objectives_count": 0, "objectives_on_track_ratio": "--"}])
    def test_teams_status(self):
        self.assertEqual(self.teams_analysis_status, "OK")

    def test_teams(self):
        self.assertListEqual(self.teams_analysis_data["teams"], 
                             [{"team_leader": "Johnson", "members": ["Navneet Menon"]},
                             {"team_leader": "Navneet", "members": []}])