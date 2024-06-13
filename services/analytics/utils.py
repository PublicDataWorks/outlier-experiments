from typing import NamedTuple


def format_metric_by_audience_segment(metrics):
    metric_report = ""
    for metric in metrics:
        metric_report += f"| - {metric[1].ljust(28)} | {str(metric[2]).ljust(4)} |\n"
    return metric_report.strip() + "\n" if metric_report else ""


def format_conversation_for_report(conversations):
    conversation_report = ""
    for result in conversations:
        conversation_report += f"| - {result[0].ljust(28)} | {str(result[1]).ljust(4)} |\n"
    return conversation_report.strip() + "\n" if conversation_report else ""


def format_lookup_history(metrics):
    lookup_history_report = ""
    for metric in metrics:
        lookup_history_report += (
            f"| {map_status(metric[0]).ljust(28)} | {str(metric[1]).ljust(5)} |\n"
        )
    return lookup_history_report.strip() + "\n" if lookup_history_report else ""


def format_geographic_regions(zipcodes):
    geographic_regions_table = ""
    for result in zipcodes:
        geographic_regions_table += f"| {str(result[0]).ljust(28)} | {str(result[1]).ljust(4)} |\n"
    return geographic_regions_table.strip() + "\n" if geographic_regions_table else ""


def to_pascal_case(string):
    return " ".join(word.capitalize() for word in string.lower().split("_"))


def map_status(raw_status):
    if raw_status == "OK":
        return "No Tax Debt"
    else:
        return to_pascal_case(raw_status)


def process_conversation_metrics(data):
    total_broadcasts = (
        data["broadcasts"]["count"]
        if isinstance(data["broadcasts"], dict) and data["broadcasts"]
        else 0
    )
    total_text_ins = (
        data["text_ins"]["count"] if isinstance(data["text_ins"], dict) and data["text_ins"] else 0
    )
    failed_deliveries = (
        data["failed_deliveries"]["count"]
        if isinstance(data["failed_deliveries"], dict) and data["failed_deliveries"]
        else 0
    )
    total_unsubscribed_messages = (
        sum(int(conversation["count"]) for conversation in data["unsubscribed_messages"])
        if data["unsubscribed_messages"]
        else 0
    )
    total_replies = (
        sum(int(conversation["count"]) for conversation in data["replies"])
        if data["replies"]
        else 0
    )
    total_report_conversations = (
        sum(int(conversation["count"]) for conversation in data["report_conversations"])
        if data["report_conversations"]
        else 0
    )

    conversation_metrics = {
        "conversation_starters_sent": total_broadcasts,
        "broadcast_replies": total_replies,
        "text_ins": total_text_ins,
        "reporter_conversations": total_report_conversations,
        "unsubscribes": total_unsubscribed_messages,
        "failed_deliveries": failed_deliveries,
    }

    return conversation_metrics


def process_lookup_history(lookup_data):
    # Initialize the status counts
    status_counts = {
        "REGISTERED": 0,
        "UNREGISTERED": 0,
        "TAX_DEBT": 0,
        "NO_TAX_DEBT": 0,
        "COMPLIANT": 0,
        "FORECLOSED": 0,
    }

    # Map the fetched data to status_counts
    for row in lookup_data:
        status = row["status"]
        count = row["count"]
        if status in status_counts:
            status_counts[status] = count

    return status_counts


def process_conversation_outcomes(outcomes):
    outcome_counts = {
        "user satisfaction": 0,
        "problem addressed": 0,
        "unsatisfied": 0,
        "accountability gap": 0,
        "crisis averted": 0,
        "future keyword": 0,
        "source": 0,
    }

    # Map the fetched data to outcome_counts
    for row in outcomes:
        label_name = row["label_name"]
        count = row["count"]
        if label_name in outcome_counts:
            outcome_counts[label_name] = count

    return outcome_counts


def process_audience_segment_related_data(data):
    # Initialize the segment counts
    segment_counts = {"Proactive": 0, "Receptive": 0, "Connected": 0, "Passive": 0, "Inactive": 0}

    # Map the fetched data to segment_counts
    for row in data:
        segment_name = row["name"]
        count = row["count"]
        if segment_name in segment_counts:
            segment_counts[segment_name] = count

    return segment_counts


def generate_geographic_region_markdown(zip_codes):
    zip_code_section = format_geographic_regions(zip_codes)
    if zip_code_section.strip():
        return (
            "### Data Lookups by Geographic Regions (Top 5 ZIP Codes)\n"
            "| **ZIP Code** | **Count** |\n"
            "|--------------|-------|\n"
            f"{zip_code_section}"
        )
    return ""


def generate_lookup_history_markdown(status_counts):
    return (
        "### Data Lookups by Property Status\n"
        "| Status                         | Count |\n"
        "|------------------------------- |-------|\n"
        f"| Registered             | {status_counts['REGISTERED']} |\n"
        f"| Unregistered            | {status_counts['UNREGISTERED']}  |\n"
        f"| Tax Debt                | {status_counts['TAX_DEBT']} |\n"
        f"| No Tax Debt            | {status_counts['NO_TAX_DEBT']} |\n"
        f"| Compliant               | {status_counts['COMPLIANT']} |\n"
        f"| Foreclosed              | {status_counts['FORECLOSED']} |\n"
    )


def generate_conversation_outcomes_markdown(outcome_counts):
    return (
        "### Conversation Outcomes\n"
        "| Outcome                         | Count |\n"
        "|-------------------------------  |-------|\n"
        f"| User Satisfaction             | {outcome_counts['user satisfaction']} |\n"
        f"| Problem Addressed             | {outcome_counts['problem addressed']}  |\n"
        f"| Crisis Averted                | {outcome_counts['crisis averted']} |\n"
        f"| Accountability Gap            | {outcome_counts['accountability gap']} |\n"
        f"| Source                        | {outcome_counts['source']} |\n"
        f"| Unsatisfied                    | {outcome_counts['unsatisfied']} |\n"
        f"| Future Keyword                | {outcome_counts['future keyword']} |\n"
    )


def generate_data_by_audience_segment_markdown(segment_counts):
    return (
        "### Broadcast Replies by Audience Segment\n"
        "| Segment                         | Count |\n"
        "|-------------------------------  |-------|\n"
        f"| Proactive              | {segment_counts['Proactive']} |\n"
        f"| Receptive             | {segment_counts['Receptive']}  |\n"
        f"| Connected                | {segment_counts['Connected']} |\n"
        f"| Passive            | {segment_counts['Passive']} |\n"
        f"| Inactive                        | {segment_counts['Inactive']} |\n"
    )


def get_current_date_formatted_for_weekly_report():
    # Placeholder function: Replace with the actual implementation
    from datetime import date

    return date.today().strftime("%B %d, %Y")


def generate_intro_section():
    report_date = get_current_date_formatted_for_weekly_report()
    return f"# Weekly Summary Report ({report_date})"


def generate_major_themes_section():
    return (
        "## Summary of Major Themes/Topics\n"
        "- **User Satisfaction**: Significant number of users expressed satisfaction with the resources provided.\n"
        "- **Problem Addressed**: Numerous reports of problems addressed successfully.\n"
        "- **Crisis Averted**: Notable increase in crisis averted scenarios.\n"
        "- **Property Status Inquiries**: Frequent inquiries about property status, particularly regarding tax debt and compliance issues.\n"
        "- **Accountability Initiatives**: Positive feedback on accountability initiatives, with some users highlighting persistent issues.\n"
    )


def generate_conversation_metrics_section(conversation_metrics):
    return (
        "### Conversation Metrics\n"
        "| Metric                         | Count |\n"
        "|------------------------------- |-------|\n"
        f"| Conversation Starters Sent     | {conversation_metrics['conversation_starters_sent']} |\n"
        f"| Broadcast replies              | {conversation_metrics['broadcast_replies']}  |\n"
        f"| Text-ins                       | {conversation_metrics['text_ins']} |\n"
        f"| Reporter conversations         | {conversation_metrics['reporter_conversations']} |\n"
        f"| Failed Deliveries              | {conversation_metrics['failed_deliveries']} |\n"
        f"| Unsubscribes                   | {conversation_metrics['unsubscribes']} |\n"
    )


class FetchDataResult(NamedTuple):
    unsubscribed_messages: int
    broadcasts: int
    failed_deliveries: int
    text_ins: int
    impact_conversations: int
    replies: int
    report_conversations: int
    lookup_history: int
    zip_codes: int

    def __getitem__(self, key):
        return getattr(self, key)