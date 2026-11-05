<!--
  Copyright (C) 2026 Dan Brown
  SPDX-License-Identifier: GPL-3.0-or-later
-->
<template>
  <cv-grid fullWidth>
    <cv-row>
      <cv-column class="page-title">
        <h2>{{ $t("zones.title") }}</h2>
      </cv-column>
    </cv-row>
    <cv-row v-if="error.load">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('action.list-zones')"
          :description="error.load"
          :showCloseButton="false"
        />
      </cv-column>
    </cv-row>
    <cv-row v-if="error.action">
      <cv-column>
        <NsInlineNotification
          kind="error"
          :title="$t('error.error')"
          :description="error.action"
          @close="error.action = ''"
        />
      </cv-column>
    </cv-row>
    <cv-row v-if="glue.length">
      <cv-column>
        <NsInlineNotification
          kind="warning"
          :title="$t('zones.glue_title')"
          :description="glueText"
          @close="glue = []"
        />
      </cv-column>
    </cv-row>
    <cv-row v-if="isPrimary && !standby">
      <cv-column>
        <NsButton
          kind="primary"
          :icon="Add20"
          class="mg-bottom-md"
          @click="showAdd"
        >
          {{ $t("zones.add_zone") }}
        </NsButton>
      </cv-column>
    </cv-row>
    <cv-row>
      <cv-column>
        <cv-tile light>
          <cv-skeleton-text
            v-if="loading.load"
            :paragraph="true"
            :line-count="4"
          />
          <NsEmptyState
            v-else-if="!zones.length"
            :title="$t('zones.no_zones')"
          />
          <cv-data-table v-else :columns="columns" ref="zones">
            <template slot="data">
              <cv-data-table-row v-for="z in zones" :key="z.zone">
                <cv-data-table-cell>
                  <cv-link @click.prevent="openRecords(z.zone)" href="#">
                    {{ z.zone }}
                  </cv-link>
                </cv-data-table-cell>
                <cv-data-table-cell>{{ z.serial }}</cv-data-table-cell>
                <cv-data-table-cell>
                  <cv-tag
                    :kind="z.dnssec ? 'green' : 'gray'"
                    :label="
                      z.dnssec ? $t('zones.signed') : $t('zones.unsigned')
                    "
                  />
                </cv-data-table-cell>
                <cv-data-table-cell v-if="isPrimary">
                  <NsButton
                    kind="ghost"
                    size="sm"
                    :icon="Settings20"
                    @click="showDetails(z)"
                  >
                    {{ $t("zones.dnssec") }}
                  </NsButton>
                  <NsButton
                    v-if="!standby"
                    kind="ghost"
                    size="sm"
                    :icon="TrashCan20"
                    @click="zoneToRemove = z"
                  >
                    {{ $t("zones.remove") }}
                  </NsButton>
                </cv-data-table-cell>
                <cv-data-table-cell v-else>
                  {{
                    z.transferred
                      ? $t("zones.transferred")
                      : $t("zones.waiting")
                  }}
                </cv-data-table-cell>
              </cv-data-table-row>
            </template>
          </cv-data-table>
        </cv-tile>
      </cv-column>
    </cv-row>

    <!-- add zone -->
    <NsModal
      :visible="isAddShown"
      :primary-button-disabled="loading.add"
      @modal-hidden="isAddShown = false"
      @primary-click="addZone"
    >
      <template slot="title">{{ $t("zones.add_zone") }}</template>
      <template slot="content">
        <cv-form @submit.prevent="addZone">
          <NsTextInput
            v-model.trim="add.zone"
            :label="$t('zones.zone_name')"
            :helper-text="$t('zones.zone_name_helper')"
            :invalid-message="error.zone"
            data-modal-primary-focus
            ref="zone"
          />
          <NsToggle
            v-model="add.dnssec"
            value="dnssec"
            :form-item="true"
            :label="$t('zones.enable_dnssec')"
          >
            <template slot="text-left">{{ $t("settings.disabled") }}</template>
            <template slot="text-right">{{ $t("settings.enabled") }}</template>
          </NsToggle>
          <cv-select
            v-if="add.dnssec"
            v-model="add.denial"
            :label="$t('zones.denial')"
          >
            <cv-select-option value="nsec3">NSEC3</cv-select-option>
            <cv-select-option value="nsec">NSEC</cv-select-option>
          </cv-select>
        </cv-form>
      </template>
      <template slot="secondary-button">{{
        core.$t("common.cancel")
      }}</template>
      <template slot="primary-button">{{ $t("zones.add_zone") }}</template>
    </NsModal>

    <!-- DNSSEC details -->
    <NsModal
      :visible="!!details"
      @modal-hidden="closeDetails"
      @primary-click="closeDetails"
    >
      <template slot="title">{{ details ? details.zone : "" }}</template>
      <template slot="content">
        <template v-if="details">
          <NsToggle
            :value="'details-dnssec'"
            :form-item="true"
            :label="$t('zones.enable_dnssec')"
            v-model="details.dnssec"
            :disabled="loading.details || standby || details.confirmDisable"
            @change="changeDnssec"
          >
            <template slot="text-left">{{ $t("settings.disabled") }}</template>
            <template slot="text-right">{{ $t("settings.enabled") }}</template>
          </NsToggle>
          <template v-if="details.confirmDisable">
            <NsInlineNotification
              kind="warning"
              :title="$t('zones.disable_title')"
              :description="$t('zones.disable_warning')"
              :showCloseButton="false"
            />
            <NsButton
              kind="danger"
              :icon="TrashCan20"
              :loading="loading.details"
              :disabled="loading.details"
              class="mg-right-sm"
              @click="disableDnssec"
            >
              {{ $t("zones.disable_confirm") }}
            </NsButton>
            <NsButton
              kind="ghost"
              :disabled="loading.details"
              @click="details = { ...details, confirmDisable: false }"
            >
              {{ core.$t("common.cancel") }}
            </NsButton>
          </template>
          <NsInlineNotification
            v-if="details.wasSigned"
            kind="warning"
            :title="$t('zones.ds_warning_title')"
            :description="$t('zones.ds_warning')"
            :showCloseButton="false"
          />
          <template
            v-if="
              details.ds_records &&
              details.ds_records.length &&
              !details.confirmDisable
            "
          >
            <p class="ds-intro">{{ $t("zones.ds_intro") }}</p>
            <NsCodeSnippet
              v-for="ds in details.ds_records"
              :key="ds"
              :copyTooltip="core.$t('common.copy_to_clipboard')"
              :copy-feedback="core.$t('common.copied_to_clipboard')"
              :feedback-aria-label="core.$t('common.copied_to_clipboard')"
              :wrap-text="true"
              :moreText="core.$t('common.show_more')"
              :lessText="core.$t('common.show_less')"
              light
              hideExpandButton
              >{{ ds }}</NsCodeSnippet
            >
            <NsButton
              kind="ghost"
              :icon="Search20"
              :loading="loading.ds"
              @click="checkDs"
            >
              {{ $t("zones.check_ds") }}
            </NsButton>
            <div v-if="details.dsChecked">
              {{ $t("zones.ds_status_" + details.dsPublished) }}
            </div>
          </template>
          <NsInlineNotification
            v-if="error.details"
            kind="error"
            :title="$t('error.error')"
            :description="error.details"
            :showCloseButton="false"
          />
        </template>
      </template>
      <template slot="primary-button">{{ core.$t("common.close") }}</template>
    </NsModal>

    <!-- remove zone -->
    <NsDangerDeleteModal
      :isShown="!!zoneToRemove"
      :name="zoneToRemove ? zoneToRemove.zone : ''"
      :title="$t('zones.remove_zone')"
      :warning="core.$t('common.please_read_carefully')"
      :description="removeDescription"
      :typeToConfirm="
        core.$t('common.type_to_confirm', {
          name: zoneToRemove ? zoneToRemove.zone : '',
        })
      "
      :isErrorShown="false"
      @hide="zoneToRemove = null"
      @confirmDelete="removeZone"
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
  name: "Zones",
  mixins: [moduleTask, IconService, QueryParamService, PageTitleService],
  pageTitle() {
    return this.$t("zones.title") + " - " + this.appName;
  },
  data() {
    return {
      q: { page: "zones" },
      urlCheckInterval: null,
      isPrimary: false,
      standby: false,
      zones: [],
      glue: [],
      glueZone: "",
      isAddShown: false,
      add: { zone: "", dnssec: false, denial: "nsec3" },
      details: null,
      zoneToRemove: null,
      loading: { load: true, add: false, details: false, ds: false },
      error: { load: "", action: "", zone: "", details: "" },
    };
  },
  computed: {
    columns() {
      return [
        this.$t("zones.zone"),
        this.$t("zones.serial"),
        this.$t("zones.dnssec"),
        this.isPrimary ? "" : this.$t("zones.transfer"),
      ];
    },
    glueText() {
      return this.glue
        .map(
          (g) =>
            `${g.ns_name}: ${
              g.addresses.join(", ") || this.$t("zones.no_address")
            }`
        )
        .join("; ");
    },
    removeDescription() {
      return this.zoneToRemove && this.zoneToRemove.dnssec
        ? this.$t("zones.remove_signed_warning")
        : this.$t("zones.remove_warning");
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
    async load() {
      this.loading.load = true;
      this.error.load = "";
      try {
        const config = await this.runTask("get-configuration");
        this.isPrimary = config.role === "primary";
        this.standby = config.standby;
        if (config.configured) {
          this.zones = (await this.runTask("list-zones")).zones;
        }
      } catch (failure) {
        this.error.load = this.taskErrorText(failure);
      }
      this.loading.load = false;
    },
    openRecords(zone) {
      this.core.$router.push(
        `/apps/${this.instanceName}?page=records&zone=${encodeURIComponent(
          zone
        )}`
      );
    },
    showAdd() {
      this.add = { zone: "", dnssec: false, denial: "nsec3" };
      this.error.zone = "";
      this.isAddShown = true;
    },
    async addZone() {
      this.error.zone = "";
      if (!this.add.zone) {
        this.error.zone = this.$t("common.required");
        return;
      }
      this.loading.add = true;
      try {
        const out = await this.runTask(
          "add-zone",
          this.add,
          this.$t("zones.adding", { zone: this.add.zone })
        );
        this.glue = out.glue;
        this.glueZone = out.zone;
        this.isAddShown = false;
        await this.load();
      } catch (failure) {
        this.error.zone = this.taskErrorText(failure);
      }
      this.loading.add = false;
    },
    async showDetails(zone) {
      this.error.details = "";
      try {
        const info = await this.runTask("get-zone", { zone: zone.zone });
        this.details = { ...info, wasSigned: false, dsChecked: false };
      } catch (failure) {
        this.error.action = this.taskErrorText(failure);
      }
    },
    closeDetails() {
      this.details = null;
      this.load();
    },
    async changeDnssec() {
      // the toggle's change event can fire before v-model has updated
      await this.$nextTick();
      if (this.details.dnssec) {
        await this.applyDnssec(true);
      } else {
        // Turning it off deletes the keys: ask first (DESIGN 7.4)
        this.details = { ...this.details, dnssec: true, confirmDisable: true };
      }
    },
    disableDnssec() {
      return this.applyDnssec(false);
    },
    async applyDnssec(wanted) {
      this.loading.details = true;
      this.error.details = "";
      const wasEnabled = !wanted;
      try {
        const info = await this.runTask(
          "update-zone",
          { zone: this.details.zone, dnssec: wanted },
          this.$t("zones.updating", { zone: this.details.zone })
        );
        this.details = {
          ...info,
          wasSigned: wasEnabled,
          dsChecked: false,
          confirmDisable: false,
        };
      } catch (failure) {
        this.error.details = this.taskErrorText(failure);
        this.details = { ...this.details, dnssec: wasEnabled };
      }
      this.loading.details = false;
    },
    async checkDs() {
      this.loading.ds = true;
      try {
        const out = await this.runTask("check-zone-ds", {
          zone: this.details.zone,
        });
        this.details = {
          ...this.details,
          dsChecked: true,
          dsPublished: String(out.published),
        };
      } catch (failure) {
        this.error.details = this.taskErrorText(failure);
      }
      this.loading.ds = false;
    },
    async removeZone() {
      const zone = this.zoneToRemove.zone;
      this.zoneToRemove = null;
      if (this.glueZone === zone) {
        this.glue = [];
      }
      try {
        await this.runTask(
          "remove-zone",
          { zone },
          this.$t("zones.removing", { zone })
        );
      } catch (failure) {
        this.error.action = this.taskErrorText(failure);
      }
      await this.load();
    },
  },
};
</script>

<style scoped lang="scss">
@import "../styles/carbon-utils";
.ds-intro {
  margin: 1rem 0 0.5rem;
}
</style>
