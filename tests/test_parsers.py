from io_career.parsers.common import parse_json_api, parse_workday_api


def test_parse_workday_api_filters_titles():
    source = {
        "source_url": "https://example.com/jobs",
        "options": {
            "title_keyword_any": ["intern", "assistant"],
            "job_host": "https://example.com",
        },
    }
    payload = {
        "jobPostings": [
            {
                "title": "Intern, Communications",
                "externalPath": "/job/a",
                "locationsText": "Geneva",
                "postedOn": "Posted Today",
                "bulletFields": ["JR123"],
            },
            {
                "title": "Senior Director",
                "externalPath": "/job/b",
            },
        ]
    }
    rows = parse_workday_api(source, __import__("json").dumps(payload))
    assert len(rows) == 1
    assert rows[0]["job_url"] == "https://example.com/job/a"


def test_parse_json_api_supports_list_paths_and_templates():
    source = {
        "source_url": "https://example.com/api",
        "options": {
            "data_path": "data.result",
            "job_url_template": "https://example.com/job/{jobId}",
            "field_map": {
                "job_title": "jobCodeTitle",
                "location": "dutyStation.0.description",
                "job_url": "url",
            },
        },
    }
    payload = {
        "data": {
            "result": [
                {
                    "jobId": 123,
                    "jobCodeTitle": "INTERN - IT",
                    "dutyStation": [{"description": "New York"}],
                },
            ]
        }
    }
    rows = parse_json_api(source, __import__("json").dumps(payload))
    assert rows[0]["location"] == "New York"
    assert rows[0]["job_url"] == "https://example.com/job/123"


def test_parse_oracle_ce_api_basic():
    from io_career.parsers.common import parse_oracle_ce_api

    source = {
        "options": {
            "title_keyword_any": ["intern"],
            "job_url_template": "https://example.com/jobs/{Id}",
        }
    }
    payload = {
        "items": [
            {
                "requisitionList": [
                    {
                        "Id": "32317",
                        "Title": "Internship Roster",
                        "PrimaryLocation": "Cairo, Egypt",
                        "PostingEndDate": "2026-03-30",
                        "PostedDate": "2026-03-03",
                        "ShortDescriptionStr": "Duties",
                    },
                    {"Id": "999", "Title": "Senior Director"},
                ]
            }
        ]
    }

    rows = parse_oracle_ce_api(source, __import__("json").dumps(payload))
    assert len(rows) == 1
    assert rows[0]["job_url"] == "https://example.com/jobs/32317"
