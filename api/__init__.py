"""Hirespy REST API."""

from hirespy.api.resources import get_resources
from hirespy.api.datasets import get_datasets
from hirespy.api.datasets import post_dataset
from hirespy.api.datasets import delete_dataset
# from hirespy.api.tissueUrl import get_tissue_url
from hirespy.api.request import attr_request
from hirespy.api.stats import stats_post, stats_get, stats_plot
from hirespy.api.options import option_term, option_donor
# from hirespy.api.json import get_json