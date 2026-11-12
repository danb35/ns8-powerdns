<!--
  Copyright (C) 2026 Dan Brown
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("replication.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.load">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.list-secondaries')"
          :description="error.load"
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
            :line-count="3"
          />
          <NsEmptyState
            v-else-if="isSecondary"
            :title="$t('replication.on_secondary')"
          >
            <template #description>
              {{ $t("replication.on_secondary_description") }}
            </template>
          </NsEmptyState>
          <NsEmptyState
            v-else-if="!secondaries.length"
            :title="$t('replication.no_secondaries')"
          >
            <template #description>
              {{ $t("replication.no_secondaries_description") }}
            </template>
          </NsEmptyState>
          <cv-data-table v-else :columns="columns">
            <template slot="data">
              <cv-data-table-row v-for="s in secondaries" :key="s.module_id">
                <cv-data-table-cell>{{ s.module_id }}</cv-data-table-cell>
                <cv-data-table-cell>{{ s.address }}</cv-data-table-cell>
                <cv-data-table-cell>{{ s.ns_name }}</cv-data-table-cell>
                <cv-data-table-cell>
                  <cv-tag :kind="stateKind(s)" :label="stateLabel(s)" />
                </cv-data-table-cell>
                <cv-data-table-cell>
                  <NsButton
                    v-if="!s.reachable"
                    kind="ghost"
                    size="sm"
                    :icon="TrashCan20"
                    @click="toRemove = s"
                  >
                    {{ $t("replication.remove") }}
                  </NsButton>
                </cv-data-table-cell>
              </cv-data-table-row>
            </template>
          </cv-data-table>
        </cv-tile>
      </cv-column>
    </cv-row>
    <!-- external secondaries (DESIGN 6.6) -->
    <cv-row v-if="!loading.load && !isSecondary && isPrimary">
      <cv-column class="page-subtitle">
        <h4>{{ $t("external.title") }}</h4>
        <p class="mg-bottom-md external-intro">{{ $t("external.intro") }}</p>
      </cv-column>
    </cv-row>
    <cv-row v-if="!loading.load && !isSecondary && isPrimary">
      <cv-column>
        <NsButton
          kind="secondary"
          :icon="Add20"
          :disabled="standby"
          @click="openAdd"
          class="mg-bottom-md"
        >
          {{ $t("external.add") }}
        </NsButton>
        <cv-tile light>
          <NsEmptyState v-if="!external.length" :title="$t('external.none')">
            <template #description>
              {{ $t("external.none_description") }}
            </template>
          </NsEmptyState>
          <cv-data-table v-else :columns="externalColumns">
            <template slot="data">
              <cv-data-table-row v-for="x in external" :key="x.id">
                <cv-data-table-cell>{{ x.name }}</cv-data-table-cell>
                <cv-data-table-cell>{{
                  x.notify.join(", ")
                }}</cv-data-table-cell>
                <cv-data-table-cell>
                  <template v-if="x.advertise && x.ns_names.length">{{
                    x.ns_names.join(", ")
                  }}</template>
                  <template v-else>{{
                    $t("external.not_advertised")
                  }}</template>
                </cv-data-table-cell>
                <cv-data-table-cell>
                  <cv-tag
                    :kind="x.auth === 'ip' ? 'magenta' : 'cool-gray'"
                    :label="
                      x.auth === 'ip'
                        ? $t('external.auth_ip_short')
                        : $t('external.auth_tsig_short')
                    "
                  />
                </cv-data-table-cell>
                <cv-data-table-cell>{{
                  x.zones === "all"
                    ? $t("external.zones_all_short", { count: x.zones_total })
                    : x.zones_total
                }}</cv-data-table-cell>
                <cv-data-table-cell>
                  <cv-tag
                    :kind="externalStateKind(x)"
                    :label="externalStateLabel(x)"
                  />
                </cv-data-table-cell>
                <cv-data-table-cell>
                  <cv-overflow-menu :flip-menu="true">
                    <cv-overflow-menu-item
                      :disabled="standby"
                      @click="openEdit(x)"
                      >{{ $t("external.edit") }}</cv-overflow-menu-item
                    >
                    <cv-overflow-menu-item
                      v-if="x.auth === 'tsig'"
                      @click="showKey(x)"
                      >{{ $t("external.show_key") }}</cv-overflow-menu-item
                    >
                    <cv-overflow-menu-item
                      danger
                      :disabled="standby"
                      @click="toRemoveExternal = x"
                      >{{ $t("external.remove") }}</cv-overflow-menu-item
                    >
                  </cv-overflow-menu>
                </cv-data-table-cell>
              </cv-data-table-row>
            </template>
          </cv-data-table>
        </cv-tile>
      </cv-column>
    </cv-row>

    <!-- add or edit an external secondary -->
    <NsModal
      size="default"
      :visible="!!form"
      :primary-button-disabled="loading.save"
      @modal-hidden="form = null"
      @primary-click="save"
    >
      <template slot="title">{{
        form && form.id ? $t("external.edit_title") : $t("external.add")
      }}</template>
      <template slot="content">
        <cv-form v-if="form" @submit.prevent="save">
          <NsTextInput
            v-model.trim="form.name"
            :label="$t('external.name')"
            :helper-text="$t('external.name_helper')"
            :invalid-message="error.name"
            data-modal-primary-focus
          />
          <cv-text-area
            v-model="form.notify"
            :label="$t('external.notify')"
            :helper-text="$t('external.notify_helper')"
            :invalid-message="error.notify"
            :rows="2"
          />
          <cv-text-area
            v-model="form.ns_names"
            :label="$t('external.ns_names')"
            :helper-text="$t('external.ns_names_helper')"
            :invalid-message="error.ns_names"
            :rows="2"
          />
          <NsToggle
            v-model="form.advertise"
            value="advertise"
            :form-item="true"
            :label="$t('external.advertise')"
          >
            <template slot="text-left">{{ $t("settings.disabled") }}</template>
            <template slot="text-right">{{ $t("settings.enabled") }}</template>
          </NsToggle>

          <cv-radio-group
            :legend="$t('external.zones')"
            :vertical="true"
            class="mg-bottom-md"
          >
            <cv-radio-button
              v-model="form.zonesMode"
              name="zones-mode"
              value="all"
              :label="$t('external.zones_all')"
            />
            <cv-radio-button
              v-model="form.zonesMode"
              name="zones-mode"
              value="selected"
              :label="$t('external.zones_selected')"
            />
          </cv-radio-group>
          <div v-if="form.zonesMode === 'selected'" class="mg-bottom-md">
            <p v-if="!zones.length">{{ $t("external.no_zones") }}</p>
            <cv-checkbox
              v-for="z in zones"
              :key="z"
              v-model="form.zones"
              :value="z"
              :label="z"
            />
            <div v-if="error.zones" class="validation-error">
              {{ error.zones }}
            </div>
          </div>

          <cv-radio-group
            :legend="$t('external.auth')"
            :vertical="true"
            class="mg-bottom-md"
          >
            <cv-radio-button
              v-model="form.auth"
              name="auth"
              value="tsig"
              :label="$t('external.auth_tsig')"
            />
            <cv-radio-button
              v-model="form.auth"
              name="auth"
              value="ip"
              :label="$t('external.auth_ip')"
            />
          </cv-radio-group>

          <template v-if="form.auth === 'tsig'">
            <cv-radio-group
              v-if="form.id && form.hadKey"
              :legend="$t('external.key')"
              :vertical="true"
              class="mg-bottom-md"
            >
              <cv-radio-button
                v-model="form.keyMode"
                name="key-mode"
                value="keep"
                :label="$t('external.key_keep')"
              />
              <cv-radio-button
                v-model="form.keyMode"
                name="key-mode"
                value="generate"
                :label="$t('external.key_generate_new')"
              />
              <cv-radio-button
                v-model="form.keyMode"
                name="key-mode"
                value="paste"
                :label="$t('external.key_paste')"
              />
            </cv-radio-group>
            <cv-radio-group
              v-else
              :legend="$t('external.key')"
              :vertical="true"
              class="mg-bottom-md"
            >
              <cv-radio-button
                v-model="form.keyMode"
                name="key-mode"
                value="generate"
                :label="$t('external.key_generate')"
              />
              <cv-radio-button
                v-model="form.keyMode"
                name="key-mode"
                value="paste"
                :label="$t('external.key_paste')"
              />
            </cv-radio-group>
            <template v-if="form.keyMode !== 'keep'">
              <NsTextInput
                v-model.trim="form.key_name"
                :label="$t('external.key_name')"
                :helper-text="$t('external.key_name_helper')"
                :invalid-message="error.tsig_key_name"
              />
              <cv-select
                v-model="form.algorithm"
                :label="$t('external.algorithm')"
              >
                <cv-select-option v-for="a in algorithms" :key="a" :value="a">{{
                  a
                }}</cv-select-option>
              </cv-select>
              <NsTextInput
                v-if="form.keyMode === 'paste'"
                v-model.trim="form.secret"
                type="password"
                :label="$t('external.secret')"
                :helper-text="$t('external.secret_helper')"
                :invalid-message="error.tsig_secret"
              />
            </template>
          </template>
          <template v-else>
            <NsInlineNotification
              kind="warning"
              :title="$t('external.ip_warning_title')"
              :description="$t('external.ip_warning')"
              :showCloseButton="false"
            />
            <cv-text-area
              v-model="form.transfer_from"
              :label="$t('external.transfer_from')"
              :helper-text="$t('external.transfer_from_helper')"
              :invalid-message="error.transfer_from"
              :rows="2"
            />
          </template>
          <NsInlineNotification
            v-if="error.save"
            kind="error"
            :title="$t('external.save_failed')"
            :description="error.save"
            :showCloseButton="false"
          />
        </cv-form>
      </template>
      <template slot="secondary-button">{{
        core.$t("common.cancel")
      }}</template>
      <template slot="primary-button">{{
        form && form.id ? core.$t("common.save") : $t("external.add")
      }}</template>
    </NsModal>

    <!-- the key to give the provider -->
    <NsModal
      size="default"
      :visible="!!key"
      @modal-hidden="key = null"
      @primary-click="key = null"
    >
      <template slot="title">{{
        $t("external.key_title", { name: key ? key.peer : "" })
      }}</template>
      <template slot="content">
        <template v-if="key">
          <p class="mg-bottom-md">{{ $t("external.key_intro") }}</p>
          <h6>{{ $t("external.key_name") }}</h6>
          <NsCodeSnippet
            :copyTooltip="core.$t('common.copy_to_clipboard')"
            :copy-feedback="core.$t('common.copied_to_clipboard')"
            :feedback-aria-label="core.$t('common.copied_to_clipboard')"
            light
            hideExpandButton
            >{{ key.key_name }}</NsCodeSnippet
          >
          <h6>{{ $t("external.algorithm") }}</h6>
          <NsCodeSnippet
            :copyTooltip="core.$t('common.copy_to_clipboard')"
            :copy-feedback="core.$t('common.copied_to_clipboard')"
            :feedback-aria-label="core.$t('common.copied_to_clipboard')"
            light
            hideExpandButton
            >{{ key.algorithm }}</NsCodeSnippet
          >
          <h6>{{ $t("external.secret") }}</h6>
          <NsCodeSnippet
            :copyTooltip="core.$t('common.copy_to_clipboard')"
            :copy-feedback="core.$t('common.copied_to_clipboard')"
            :feedback-aria-label="core.$t('common.copied_to_clipboard')"
            :wrap-text="true"
            light
            hideExpandButton
            >{{ key.secret }}</NsCodeSnippet
          >
          <h6>{{ $t("external.key_bind") }}</h6>
          <NsCodeSnippet
            :copyTooltip="core.$t('common.copy_to_clipboard')"
            :copy-feedback="core.$t('common.copied_to_clipboard')"
            :feedback-aria-label="core.$t('common.copied_to_clipboard')"
            :moreText="core.$t('common.show_more')"
            :lessText="core.$t('common.show_less')"
            light
            >{{ bindKey }}</NsCodeSnippet
          >
        </template>
      </template>
      <template slot="primary-button">{{ core.$t("common.close") }}</template>
    </NsModal>

    <NsDangerDeleteModal
      :isShown="!!toRemoveExternal"
      :name="toRemoveExternal ? toRemoveExternal.name : ''"
      :title="$t('external.remove_title')"
      :warning="core.$t('common.please_read_carefully')"
      :description="
        $t('external.remove_description', {
          name: toRemoveExternal ? toRemoveExternal.name : '',
        })
      "
      :typeToConfirm="
        core.$t('common.type_to_confirm', {
          name: toRemoveExternal ? toRemoveExternal.name : '',
        })
      "
      :isErrorShown="false"
      @hide="toRemoveExternal = null"
      @confirmDelete="removeExternal"
    />

    <NsDangerDeleteModal
      :isShown="!!toRemove"
      :name="toRemove ? toRemove.module_id : ''"
      :title="$t('replication.remove_title')"
      :warning="core.$t('common.please_read_carefully')"
      :description="
        $t('replication.remove_description', {
          module: toRemove ? toRemove.module_id : '',
        })
      "
      :typeToConfirm="
        core.$t('common.type_to_confirm', {
          name: toRemove ? toRemove.module_id : '',
        })
      "
      :isErrorShown="false"
      @hide="toRemove = null"
      @confirmDelete="remove"
    />
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
  name: "Replication",
  mixins: [moduleTask, IconService, QueryParamService, PageTitleService],
  pageTitle() {
    return this.$t("replication.title") + " - " + this.appName;
  },
  data() {
    return {
      q: { page: "replication" },
      urlCheckInterval: null,
      isSecondary: false,
      isPrimary: false,
      standby: false,
      secondaries: [],
      external: [],
      zones: [],
      toRemove: null,
      toRemoveExternal: null,
      form: null,
      key: null,
      algorithms: [
        "hmac-sha256",
        "hmac-sha512",
        "hmac-sha384",
        "hmac-sha224",
        "hmac-sha1",
        "hmac-md5",
      ],
      loading: { load: true, save: false },
      error: {
        load: "",
        save: "",
        name: "",
        notify: "",
        ns_names: "",
        zones: "",
        transfer_from: "",
        tsig_key_name: "",
        tsig_secret: "",
      },
    };
  },
  computed: {
    columns() {
      return [
        this.$t("replication.module"),
        this.$t("replication.address"),
        this.$t("replication.ns_name"),
        this.$t("replication.state"),
        "",
      ];
    },
    externalColumns() {
      return [
        this.$t("external.name"),
        this.$t("external.notify_short"),
        this.$t("replication.ns_name"),
        this.$t("external.auth_short"),
        this.$t("external.zones_short"),
        this.$t("replication.state"),
        "",
      ];
    },
    bindKey() {
      if (!this.key) return "";
      return `key "${this.key.key_name}" {\n  algorithm ${this.key.algorithm};\n  secret "${this.key.secret}";\n};`;
    },
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
    stateKind(s) {
      if (!s.reachable) return "red";
      return s.zones_behind.length ? "high-contrast" : "green";
    },
    stateLabel(s) {
      if (!s.reachable) return this.$t("replication.unreachable");
      return s.zones_behind.length
        ? this.$t("replication.behind", { count: s.zones_behind.length })
        : this.$t("replication.in_sync");
    },
    async load() {
      this.loading.load = true;
      this.error.load = "";
      try {
        const config = await this.runTask("get-configuration");
        this.isSecondary = config.role === "secondary";
        this.isPrimary = config.role === "primary";
        if (config.role === "primary") {
          const [list, status, zones] = await Promise.all([
            this.runTask("list-secondaries"),
            this.runTask("get-dns-status"),
            this.runTask("list-zones"),
          ]);
          this.secondaries = list.secondaries;
          this.external = list.external;
          this.standby = status.standby;
          this.zones = zones.zones.map((z) => z.zone);
        }
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      this.loading.load = false;
    },
    externalStateKind(x) {
      if (!x.zones_total) return "gray";
      if (!x.answering) return "high-contrast";
      return x.zones_behind.length ? "high-contrast" : "green";
    },
    externalStateLabel(x) {
      if (!x.zones_total) return this.$t("external.no_zones_given");
      if (!x.answering) return this.$t("external.not_answering");
      return x.zones_behind.length
        ? this.$t("replication.behind", { count: x.zones_behind.length })
        : this.$t("replication.in_sync");
    },
    clearErrors() {
      for (const k of Object.keys(this.error)) {
        if (k !== "load") this.error[k] = "";
      }
    },
    openAdd() {
      this.clearErrors();
      this.form = {
        id: "",
        name: "",
        notify: "",
        ns_names: "",
        advertise: true,
        zonesMode: "all",
        zones: [],
        auth: "tsig",
        transfer_from: "",
        keyMode: "generate",
        hadKey: false,
        key_name: "",
        algorithm: "hmac-sha256",
        secret: "",
      };
    },
    openEdit(x) {
      this.clearErrors();
      this.form = {
        id: x.id,
        name: x.name,
        notify: x.notify.join("\n"),
        ns_names: x.ns_names.join("\n"),
        advertise: x.advertise,
        zonesMode: x.zones === "all" ? "all" : "selected",
        zones: x.zones === "all" ? [] : [...x.zones],
        auth: x.auth,
        transfer_from: x.transfer_from.join("\n"),
        keyMode: x.auth === "tsig" ? "keep" : "generate",
        hadKey: x.auth === "tsig",
        key_name: x.tsig_key,
        algorithm: "hmac-sha256",
        secret: "",
      };
    },
    lines(text) {
      return text
        .split(/[\s,]+/)
        .map((l) => l.trim())
        .filter((l) => l);
    },
    async save() {
      const f = this.form;
      if (!f) return;
      this.clearErrors();
      const data = {
        name: f.name,
        notify: this.lines(f.notify),
        ns_names: this.lines(f.ns_names),
        advertise: f.advertise,
        zones: f.zonesMode === "all" ? "all" : f.zones,
        auth: f.auth,
        transfer_from: f.auth === "ip" ? this.lines(f.transfer_from) : [],
      };
      if (f.auth === "tsig" && f.keyMode !== "keep") {
        data.tsig = { algorithm: f.algorithm };
        if (f.key_name) data.tsig.key_name = f.key_name;
        if (f.keyMode === "paste") data.tsig.secret = f.secret;
        if (f.id && f.keyMode === "generate") data.tsig.regenerate = true;
      }
      if (f.id) data.id = f.id;
      this.loading.save = true;
      try {
        const out = await this.runTask(
          f.id ? "update-external-secondary" : "add-external-secondary",
          data,
          f.id
            ? this.$t("external.updating", { name: f.name })
            : this.$t("external.adding", { name: f.name })
        );
        this.form = null;
        if (out.key) this.key = { ...out.key, peer: out.secondary.name };
        await this.load();
      } catch (failure) {
        if (failure.validationErrors) {
          for (const e of failure.validationErrors) {
            const text = this.$t("errors." + e.error, { value: e.value });
            if (
              this.error[e.parameter] !== undefined &&
              e.parameter !== "load"
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
    async showKey(x) {
      try {
        const out = await this.runTask("get-external-secondary-key", {
          id: x.id,
        });
        this.key = { ...out, peer: x.name };
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
    },
    async removeExternal() {
      const x = this.toRemoveExternal;
      this.toRemoveExternal = null;
      if (!x) return;
      try {
        await this.runTask(
          "remove-external-secondary",
          { id: x.id },
          this.$t("external.removing", { name: x.name })
        );
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      await this.load();
    },
    async remove() {
      const s = this.toRemove;
      this.toRemove = null;
      if (!s) return;
      try {
        await this.runTask(
          "remove-secondary",
          { module_id: s.module_id },
          this.$t("replication.removing", { module: s.module_id })
        );
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      await this.load();
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";

.external-intro {
  margin-top: 0.5rem;
}
.validation-error {
  color: $danger-01;
  font-size: 0.75rem;
}
</style>
