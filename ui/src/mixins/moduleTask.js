//
// Copyright (C) 2026 Dan Brown
// SPDX-License-Identifier: GPL-3.0-or-later
//
import to from "await-to-js";
import { mapState } from "vuex";
import { TaskService, UtilService } from "@nethserver/ns8-ui-lib";

// Runs a module action and resolves with its output. Rejects with
// { validationErrors } for a refusal the administrator can act on, or
// { message } for anything else.
export default {
  mixins: [TaskService, UtilService],
  computed: {
    ...mapState(["instanceName", "core", "appName"]),
  },
  methods: {
    runTask(action, data, title) {
      return new Promise((resolve, reject) => {
        const eventId = this.getUuid();
        const root = this.core.$root;
        const events = ["completed", "aborted", "validation-failed"].map(
          (e) => `${action}-${e}-${eventId}`
        );
        const clear = () => events.forEach((e) => root.$off(e));
        root.$once(events[0], (taskContext, taskResult) => {
          clear();
          resolve(taskResult.output);
        });
        root.$once(events[1], (taskResult) => {
          clear();
          console.error(`${action} aborted`, taskResult);
          reject({ message: this.$t("error.generic_error") });
        });
        root.$once(events[2], (validationErrors) => {
          clear();
          reject({ validationErrors });
        });
        to(
          this.createModuleTaskForApp(this.instanceName, {
            action,
            data: data || {},
            extra: {
              title: title || this.$t("action." + action),
              isNotificationHidden: !title,
              eventId,
            },
          })
        ).then(([err]) => {
          if (err) {
            clear();
            reject({ message: this.getErrorMessage(err) });
          }
        });
      });
    },
    // The text of a rejection from runTask
    taskErrorText(failure) {
      if (failure.validationErrors) {
        return failure.validationErrors
          .map((e) => {
            const text = this.$t("errors." + e.error, {
              value: e.value,
              parameter: e.parameter,
            });
            // PowerDNS says what is wrong with a record
            return e.message ? `${text} (${e.message})` : text;
          })
          .join(" ");
      }
      return failure.message;
    },
  },
};
