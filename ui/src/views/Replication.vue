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
      secondaries: [],
      toRemove: null,
      loading: { load: true },
      error: { load: "" },
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
        if (config.role === "primary") {
          this.secondaries = (
            await this.runTask("list-secondaries")
          ).secondaries;
        }
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      this.loading.load = false;
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
</style>
