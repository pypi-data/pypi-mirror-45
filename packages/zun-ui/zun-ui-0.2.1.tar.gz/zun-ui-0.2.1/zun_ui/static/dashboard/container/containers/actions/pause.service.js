/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  /**
   * @ngDoc factory
   * @name horizon.dashboard.container.containers.pause.service
   * @Description
   * pause container.
   */
  angular
    .module('horizon.dashboard.container.containers')
    .factory('horizon.dashboard.container.containers.pause.service', pauseService);

  pauseService.$inject = [
    'horizon.app.core.openstack-service-api.zun',
    'horizon.dashboard.container.containers.resourceType',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.toast.service'
  ];

  function pauseService(
    zun, resourceType, actionResult, $qExtensions, toast
  ) {

    var message = {
      success: gettext('Container %s was successfully paused.')
    };

    var service = {
      initAction: initAction,
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    // include this function in your service
    // if you plan to emit events to the parent controller
    function initAction() {
    }

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
    }

    function perform(selected) {
      // pause selected container
      return zun.pauseContainer(selected.id).then(success);

      function success() {
        toast.add('success', interpolate(message.success, [selected.name]));
        var result = actionResult.getActionResult().updated(resourceType, selected.id);
        return result.result;
      }
    }
  }
})();
