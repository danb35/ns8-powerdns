<!--
  Copyright (C) 2026 Dan Brown
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("records.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.load">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.get-records')"
          :description="error.load"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row v-if="managed">
      <cv-column>
        <NsInlineNotification
          kind="info"
          :title="$t('records.managed_title')"
          :description="$t('records.managed')"
          :actionLabel="dnshelperModule ? $t('records.open_dnshelper') : ''"
          :showCloseButton="false"
          @action="openDnshelper"
        />
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column :md="4">
        <cv-select
          v-model="zone"
          :label="$t('records.zone')"
          class="mg-bottom-md"
        >
          <cv-select-option disabled hidden value="">
            {{ $t("records.choose_zone") }}
          </cv-select-option>
          <cv-select-option v-for="z in zones" :key="z" :value="z">
            {{ z }}
          </cv-select-option>
        </cv-select>
      </cv-column>
    </cv-row>
    <cv-row v-if="editable">
      <cv-column>
        <NsButton
          kind="primary"
          :icon="Add20"
          class="mg-bottom-md"
          @click="showEdit()"
        >
          {{ $t("records.add_record") }}
        </NsButton>
      </cv-column>
    </cv-row>
    <cv-row v-if="zone">
      <cv-column>
        <cv-tile light>
          <cv-skeleton-text
            v-if="loading.load"
            :paragraph="true"
            :line-count="4"
          />
          <cv-data-table v-else :columns="columns">
            <template slot="data">
              <cv-data-table-row
                v-for="(r, i) in records"
                :key="`${r.name}-${r.type}-${i}`"
              >
                <cv-data-table-cell>{{ r.name }}</cv-data-table-cell>
                <cv-data-table-cell>{{ r.type }}</cv-data-table-cell>
                <cv-data-table-cell>{{ r.ttl }}</cv-data-table-cell>
                <cv-data-table-cell class="record-data">{{
                  r.data
                }}</cv-data-table-cell>
                <cv-data-table-cell>
                  <template v-if="editable && !isProtected(r)">
                    <NsButton
                      kind="ghost"
                      size="sm"
                      :icon="Edit20"
                      @click="showEdit(r)"
                    >
                      {{ $t("records.edit") }}
                    </NsButton>
                    <NsButton
                      kind="ghost"
                      size="sm"
                      :icon="TrashCan20"
                      @click="deleteRecord(r)"
                    >
                      {{ $t("records.delete") }}
                    </NsButton>
                  </template>
                </cv-data-table-cell>
              </cv-data-table-row>
            </template>
          </cv-data-table>
        </cv-tile>
      </cv-column>
    </cv-row>
    <NsModal
      :visible="isEditShown"
      :primary-button-disabled="loading.save"
      @modal-hidden="isEditShown = false"
      @primary-click="saveRecord"
    >
      <template slot="title">
        {{ original ? $t("records.edit_record") : $t("records.add_record") }}
      </template>
      <template slot="content">
        <cv-form @submit.prevent="saveRecord">
          <NsTextInput
            v-model.trim="form.name"
            :label="$t('records.name')"
            :helper-text="$t('records.name_helper')"
            :disabled="!!original"
          />
          <cv-select
            v-model="form.type"
            :label="$t('records.type')"
            :disabled="!!original"
          >
            <cv-select-option v-for="t in recordTypes" :key="t" :value="t">
              {{ t }}
            </cv-select-option>
          </cv-select>
          <NsTextInput
            v-model.number="form.ttl"
            type="number"
            min="1"
            :label="$t('records.ttl')"
          />
          <NsTextInput v-model="form.data" :label="$t('records.data')" />
          <NsInlineNotification
            v-if="error.save"
            kind="error"
            :title="$t('error.error')"
            :description="error.save"
            :showCloseButton="false"
          />
        </cv-form>
      </template>
      <template slot="secondary-button">{{
        core.$t("common.cancel")
      }}</template>
      <template slot="primary-button">{{ $t("records.save") }}</template>
    </NsModal>
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
  name: "Records",
  mixins: [moduleTask, IconService, QueryParamService, PageTitleService],
  pageTitle() {
    return this.$t("records.title") + " - " + this.appName;
  },
  data() {
    return {
      q: { page: "records", zone: "" },
      urlCheckInterval: null,
      zones: [],
      zone: "",
      records: [],
      editable: false,
      managed: false,
      dnshelperModule: "",
      recordTypes: [
        "A",
        "AAAA",
        "CAA",
        "CNAME",
        "HTTPS",
        "MX",
        "NS",
        "PTR",
        "SRV",
        "SVCB",
        "TXT",
      ],
      isEditShown: false,
      original: null,
      form: { name: "", type: "A", ttl: 3600, data: "" },
      loading: { load: false, save: false },
      error: { load: "", save: "" },
    };
  },
  computed: {
    columns() {
      return [
        this.$t("records.name"),
        this.$t("records.type"),
        this.$t("records.ttl"),
        this.$t("records.data"),
        "",
      ];
    },
  },
  watch: {
    zone(value) {
      this.q.zone = value;
      this.loadRecords();
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
  async created() {
    try {
      const out = await this.runTask("list-zones");
      this.zones = out.zones.map((z) => z.zone);
      const requested = this.getQueryParamsForApp().zone;
      this.zone = this.zones.includes(requested)
        ? requested
        : this.zones[0] || "";
    } catch (failure) {
      this.error.load = this.taskErrorText(failure);
    }
  },
  methods: {
    isProtected(r) {
      return r.type === "SOA" || (r.type === "NS" && r.name === "@");
    },
    async loadRecords() {
      if (!this.zone) return;
      this.loading.load = true;
      this.error.load = "";
      try {
        const out = await this.runTask("get-records", { zone: this.zone });
        this.records = out.records;
        this.editable = out.editable;
        this.managed = out.managed_by_dnshelper;
        this.dnshelperModule = out.dnshelper_module_id;
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      this.loading.load = false;
    },
    openDnshelper() {
      this.core.$router.push(
        `/apps/${this.dnshelperModule}?page=records&zone=${encodeURIComponent(
          this.zone
        )}`
      );
    },
    showEdit(record) {
      this.original = record || null;
      this.form = record
        ? { ...record }
        : { name: "", type: "A", ttl: 3600, data: "" };
      this.error.save = "";
      this.isEditShown = true;
    },
    // set-records replaces a whole RRset, so send the set's other values too
    siblings() {
      return this.records.filter(
        (r) =>
          r.name === (this.form.name || "@") &&
          r.type === this.form.type &&
          !(this.original && r.data === this.original.data)
      );
    },
    async saveRecord() {
      this.loading.save = true;
      this.error.save = "";
      const record = { ...this.form, name: this.form.name || "@" };
      const siblings = this.siblings().map((r) => ({ ...r, ttl: record.ttl }));
      try {
        await this.runTask(
          "set-records",
          { zone: this.zone, records: [...siblings, record] },
          this.$t("records.saving", { zone: this.zone })
        );
        this.isEditShown = false;
        await this.loadRecords();
      } catch (failure) {
        this.error.save = this.taskErrorText(failure);
      }
      this.loading.save = false;
    },
    async deleteRecord(r) {
      try {
        await this.runTask(
          "delete-records",
          {
            zone: this.zone,
            records: [{ name: r.name, type: r.type, data: r.data }],
          },
          this.$t("records.saving", { zone: this.zone })
        );
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      await this.loadRecords();
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";
.record-data {
  word-break: break-all;
}
</style>
