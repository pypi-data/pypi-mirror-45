"""Core functions for HealthChecker."""

# -----------------------------------------------------------------------------
# Copyright (C) 2019 HacKan (https://hackan.net)
#
# This file is part of HealthChecker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import asyncio
import concurrent.futures
import logging
from typing import Optional, Union

from .objects import ServiceStatus, ServiceStatusList
from .utils import http_get, http_request

logger = logging.getLogger(__name__)


def healthcheck(url: str, timeout: Union[float, int],
                find_data: Optional[str] = None) -> ServiceStatus:
    """Check if a URL is alive or not.

    Optionally, it checks for a string existing in the body. The OK attribute
    of the result is True if the request is OK and the string is found or False
    otherwise.

    Considers the timeout and warn if request takes longer than 60% of the time.

    Returns a ServiceStatus object with the requested URL, its status and
    checks results.
    """
    logger.info('Begin checking URL %s...', url)
    body, request_time, error = http_get(url, timeout=timeout)
    if error and request_time > timeout:
        logger.warning('Request to %s timed out taking %.2f seconds', url,
                       request_time)
    elif request_time > (0.6 * timeout):
        logger.warning('Request to %s took too long: %.2f seconds', url,
                       request_time)
    alive = not error
    ok = body.find(find_data) != -1 if find_data and alive else alive
    result = ServiceStatus(url, alive, ok)
    logger.info('Finish checking URL: %s', str(result))
    return result


async def check_urls(urls: list, timeout,
                     validations: Optional[list] = None) -> ServiceStatusList:
    """Asynchronously check given URLs status, optionally validating them."""
    statuses = ServiceStatusList()
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        loop = asyncio.get_event_loop()
        futures = []
        for index, url in enumerate(urls):
            if validations:
                try:
                    validation = validations[index]
                except IndexError:
                    validation = validations[-1]
            else:
                validation = None
            futures.append(
                loop.run_in_executor(
                    executor,
                    healthcheck,
                    url,
                    timeout,
                    validation
                )
            )
        for result in await asyncio.gather(*futures):
            statuses.append(result)
    return statuses


def notify(url: str, payload: Optional[str] = None,
           headers: Optional[dict] = None) -> bool:
    """Execute a POST request as a notification with optional data."""
    data = payload.encode('utf-8') if payload else None
    response, _, error = http_request('POST', url, timeout=5, headers=headers,
                                      data=data)
    return not error and response.ok
