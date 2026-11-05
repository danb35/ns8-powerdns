<!--
  Copyright (C) 2026 Dan Brown
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("settings.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.load">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.get-configuration')"
          :description="error.load"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row v-if="missingAddresses.length">
      <cv-column>
        <NsInlineNotification
          kind="warning"
          :title="$t('settings.missing_addresses')"
          :description="missingAddresses.join(', ')"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <cv-tile light>
          <cv-skeleton-text
            v-if="loading.load"
            :paragraph="true"
            :line-count="8"
          />
          <cv-form v-else @submit.prevent="save">
            <div class="bx--label">{{ $t("settings.role") }}</div>
            <cv-radio-group
              :vertical="true"
              class="mg-bottom-md"
            >
              <cv-radio-button
                v-model="form.role"
                name="role"
                value="primary"
                :label="$t('settings.role_primary')"
                :disabled="configured || primaries.length > 0"
              />
              <cv-radio-button
                v-model="form.role"
                name="role"
                value="secondary"
                :label="$t('settings.role_secondary')"
                :disabled="configured"
              />
            </cv-radio-group>
            <NsInlineNotification
              v-if="!configured && primaries.length"
              kind="info"
              :title="$t('settings.primary_exists_title')"
              :description="
                $t('settings.primary_exists', {
                  primary: primaries[0].module_id,
                })
              "
              :showCloseButton="false"
            />
            <cv-select
              v-if="form.role === 'secondary'"
              v-model="form.primary"
              :label="$t('settings.primary')"
              :invalid-message="error.primary"
              ref="primary"
            >
              <cv-select-option disabled hidden value="">
                {{ $t("settings.choose_primary") }}
              </cv-select-option>
              <cv-select-option
                v-for="p in primaries"
                :key="p.module_uuid"
                :value="p.module_uuid"
              >
                {{ p.ui_name ? `${p.ui_name} (${p.module_id})` : p.module_id }}
              </cv-select-option>
            </cv-select>
            <NsTextInput
              v-model.trim="form.ns_name"
              :label="$t('settings.ns_name')"
              :helper-text="$t('settings.ns_name_helper')"
              placeholder="ns1.example.com"
              :invalid-message="error.ns_name"
              ref="ns_name"
            />
            <NsToggle
              v-model="form.advertise"
              value="advertise"
              :form-item="true"
              :label="$t('settings.advertise')"
            >
              <template slot="tooltip">
                {{ $t("settings.advertise_helper") }}
              </template>
              <template slot="text-left">{{
                $t("settings.disabled")
              }}</template>
              <template slot="text-right">{{
                $t("settings.enabled")
              }}</template>
            </NsToggle>
            <div class="bx--form-item mg-bottom-md">
              <div class="bx--label">{{ $t("settings.listen_addresses") }}</div>
              <div class="bx--form__helper-text mg-bottom-sm">
                {{
                  $t("settings.listen_addresses_helper", { vpn: vpnAddress })
                }}
              </div>
              <cv-checkbox
                v-for="a in nodeAddresses"
                :key="a.address"
                v-model="form.listen_addresses"
                :value="a.address"
                :disabled="!isFree(a)"
                :label="addressLabel(a)"
              />
              <div v-if="error.listen_addresses" class="validation-error">
                {{ error.listen_addresses }}
              </div>
            </div>
            <template v-if="form.role === 'primary'">
              <NsTextInput
                v-model.trim="form.hostmaster"
                :label="$t('settings.hostmaster')"
                placeholder="hostmaster@example.com"
                :invalid-message="error.hostmaster"
                ref="hostmaster"
              />
              <NsTextInput
                v-for="t in soaTimers"
                :key="t"
                v-model.number="form['soa_' + t]"
                type="number"
                min="1"
                :label="$t('settings.soa_' + t)"
              />
            </template>
            <NsInlineNotification
              v-if="error.save"
              kind="error"
              :title="$t('action.configure-module')"
              :description="error.save"
              :showCloseButton="false"
            />
            <NsButton
              kind="primary"
              :icon="Save20"
              :loading="loading.save"
              :disabled="loading.save"
            >
              {{ $t("settings.save") }}
            </NsButton>
          </cv-form>
        </cv-tile>
      </cv-column>
    </cv-row>
  </cv-grid>
</template>

<script>
import {
  QueryParamService,
  IconService,
  PageTitleService,
} from "@nethserver/ns8-ui-lib";
import moduleTask from "../mixins/moduleTask";

export default {
  name: "Settings",
  mixins: [moduleTask, IconService, QueryParamService, PageTitleService],
  pageTitle() {
    return this.$t("settings.title") + " - " + this.appName;
  },
  data() {
    return {
      q: { page: "settings" },
      urlCheckInterval: null,
      configured: false,
      primaries: [],
      nodeAddresses: [],
      missingAddresses: [],
      vpnAddress: "",
      soaTimers: ["refresh", "retry", "expire", "minimum"],
      form: {
        role: "primary",
        primary: "",
        ns_name: "",
        advertise: true,
        listen_addresses: [],
        hostmaster: "",
        soa_refresh: 10800,
        soa_retry: 3600,
        soa_expire: 604800,
        soa_minimum: 3600,
      },
      loading: { load: true, save: false },
      error: {
        load: "",
        save: "",
        role: "",
        primary: "",
        ns_name: "",
        hostmaster: "",
        listen_addresses: "",
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.watchQueryData(vm);
      vm.urlCheckInterval = vm.initUrlBindingForApp(vm, vm.q.page);
    });
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.urlCheckInterval);
    next();
  },
  created() {
    this.load();
  },
  methods: {
    isFree(a) {
      return a.in_use_by_self || (a.udp_free && a.tcp_free);
    },
    addressLabel(a) {
      return this.isFree(a)
        ? a.address
        : this.$t("settings.address_busy", { address: a.address });
    },
    async load() {
      this.loading.load = true;
      this.error.load = "";
      try {
        const config = await this.runTask("get-configuration");
        this.configured = config.configured;
        this.primaries = config.primaries;
        this.nodeAddresses = config.node_addresses;
        this.missingAddresses = config.missing_addresses || [];
        this.vpnAddress = config.vpn_address;
        const form = { ...this.form };
        Object.keys(form).forEach((k) => {
          if (config[k] !== undefined && config[k] !== "") {
            form[k] = config[k];
          }
        });
        if (!config.configured && config.primaries.length) {
          // There can be only one primary: offer to follow it.
          form.role = "secondary";
          form.primary = config.primaries[0].module_uuid;
        }
        this.form = form;
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      this.loading.load = false;
    },
    validate() {
      this.clearErrors(this);
      const required = ["ns_name"];
      if (this.form.role === "primary") required.push("hostmaster");
      if (this.form.role === "secondary") required.push("primary");
      let ok = true;
      for (const field of required) {
        if (!this.form[field]) {
          this.error[field] = this.$t("common.required");
          if (ok) this.focusElement(field);
          ok = false;
        }
      }
      return ok;
    },
    async save() {
      if (!this.validate()) return;
      this.loading.save = true;
      const data = { ...this.form };
      if (data.role === "primary") delete data.primary;
      try {
        await this.runTask(
          "configure-module",
          data,
          this.$t("settings.configure_instance", {
            instance: this.instanceName,
          })
        );
        await this.load();
      } catch (failure) {
        if (failure.validationErrors) {
          for (const e of failure.validationErrors) {
            const text = this.$t("errors." + e.error, { value: e.value });
            if (
              this.error[e.parameter] !== undefined &&
              e.parameter !== "role"
            ) {
              this.error[e.parameter] = text;
            } else {
              this.error.save = text;
            }
          }
        } else {
          this.error.save = failure.message;
        }
      }
      this.loading.save = false;
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";
.validation-error {
  color: $danger-01;
  font-size: 0.75rem;
}
</style>
