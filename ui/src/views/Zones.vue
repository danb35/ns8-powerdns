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
                    {{ $t("zones.details") }}
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

    <!-- zone details: DNSSEC and what the registrar needs -->
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
          <template v-if="!details.confirmDisable">
            <h5 class="registrar-title">{{ $t("zones.registrar_title") }}</h5>
            <p class="registrar-intro">
              {{
                isReverse(details.zone)
                  ? $t("zones.registrar_intro_reverse")
                  : $t("zones.registrar_intro", { zone: details.zone })
              }}
            </p>
            <h6>{{ $t("zones.name_servers") }}</h6>
            <NsCodeSnippet
              :copyTooltip="core.$t('common.copy_to_clipboard')"
              :copy-feedback="core.$t('common.copied_to_clipboard')"
              :feedback-aria-label="core.$t('common.copied_to_clipboard')"
              :wrap-text="true"
              :moreText="core.$t('common.show_more')"
              :lessText="core.$t('common.show_less')"
              light
              hideExpandButton
              >{{ nameServerText }}</NsCodeSnippet
            >
            <template v-for="ns in glueServers">
              <p :key="ns.ns_name + '-intro'" class="registrar-intro">
                {{
                  publicAddresses(ns).length
                    ? $t("zones.glue_intro", { name: ns.ns_name })
                    : $t("zones.glue_no_public", { name: ns.ns_name })
                }}
              </p>
              <NsCodeSnippet
                v-if="publicAddresses(ns).length"
                :key="ns.ns_name + '-addresses'"
                :copyTooltip="core.$t('common.copy_to_clipboard')"
                :copy-feedback="core.$t('common.copied_to_clipboard')"
                :feedback-aria-label="core.$t('common.copied_to_clipboard')"
                :wrap-text="true"
                :moreText="core.$t('common.show_more')"
                :lessText="core.$t('common.show_less')"
                light
                hideExpandButton
                >{{ publicAddresses(ns).join("\n") }}</NsCodeSnippet
              >
            </template>
            <template v-if="details.ds_records && details.ds_records.length">
              <h6>{{ $t("zones.ds_title") }}</h6>
              <p class="registrar-intro">{{ $t("zones.ds_intro") }}</p>
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
              <template
                v-if="details.dnskey_records && details.dnskey_records.length"
              >
                <p class="registrar-intro">{{ $t("zones.dnskey_intro") }}</p>
                <NsCodeSnippet
                  v-for="key in details.dnskey_records"
                  :key="key"
                  :copyTooltip="core.$t('common.copy_to_clipboard')"
                  :copy-feedback="core.$t('common.copied_to_clipboard')"
                  :feedback-aria-label="core.$t('common.copied_to_clipboard')"
                  :wrap-text="true"
                  :moreText="core.$t('common.show_more')"
                  :lessText="core.$t('common.show_less')"
                  light
                  hideExpandButton
                  >{{ key }}</NsCodeSnippet
                >
              </template>
            </template>
            <NsButton
              kind="ghost"
              :icon="Search20"
              :loading="loading.check"
              :disabled="loading.check"
              class="check-button"
              @click="checkDelegation"
            >
              {{ $t("zones.check_parent") }}
            </NsButton>
            <div v-if="check" class="check-results">
              <div v-for="(line, i) in checkLines" :key="i" class="check-line">
                <cv-tag
                  :kind="
                    line.ok === true
                      ? 'green'
                      : line.ok === false
                      ? 'red'
                      : 'gray'
                  "
                  :label="
                    line.ok === true
                      ? $t('zones.check_ok')
                      : line.ok === false
                      ? $t('zones.check_problem')
                      : $t('zones.check_unknown')
                  "
                />
                <span>{{ line.text }}</span>
              </div>
              <p class="check-delay">{{ $t("zones.check_delay") }}</p>
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
      isAddShown: false,
      add: { zone: "", dnssec: false, denial: "nsec3" },
      details: null,
      check: null,
      zoneToRemove: null,
      loading: { load: true, add: false, details: false, check: false },
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
    nameServers() {
      return (this.details && this.details.name_servers) || [];
    },
    nameServerText() {
      return this.nameServers.map((ns) => ns.ns_name).join("\n");
    },
    glueServers() {
      return this.nameServers.filter((ns) => ns.glue);
    },
    checkLines() {
      const c = this.check;
      if (!c) {
        return [];
      }
      const t = (key, values) => this.$t("zones." + key, values);
      const list = (names) => names.join(", ") || t("check_nothing");
      const lines = [];
      // Name servers at the parent
      if (c.delegated === null) {
        lines.push({ ok: null, text: t("check_no_parent") });
      } else if (!c.delegated) {
        lines.push({
          ok: false,
          text: t("check_ns_none", { parent: c.parent }),
        });
      } else if (!c.ns_missing.length && !c.ns_extra.length) {
        lines.push({ ok: true, text: t("check_ns_ok", { parent: c.parent }) });
      } else {
        let text = t("check_ns_differ", {
          parent: c.parent,
          published: list(c.ns_published),
        });
        if (c.ns_missing.length) {
          text += " " + t("check_ns_missing", { names: list(c.ns_missing) });
        }
        if (c.ns_extra.length) {
          text += " " + t("check_ns_extra", { names: list(c.ns_extra) });
        }
        lines.push({ ok: false, text });
      }
      // Glue
      for (const g of c.glue) {
        lines.push(
          g.ok
            ? { ok: true, text: t("check_glue_ok", { name: g.ns_name }) }
            : {
                ok: false,
                text: t("check_glue_bad", {
                  name: g.ns_name,
                  published: list(g.published),
                  expected: list(g.expected),
                }),
              }
        );
      }
      // DS
      if (c.ds_ok === null) {
        lines.push({ ok: null, text: t("check_ds_unknown") });
      } else if (c.signed) {
        if (c.ds_ok) {
          lines.push({ ok: true, text: t("check_ds_ok") });
        } else if (!c.ds_published.length) {
          lines.push({ ok: false, text: t("check_ds_missing") });
        } else {
          lines.push({ ok: false, text: t("check_ds_stale") });
        }
      } else if (!c.ds_ok) {
        lines.push({ ok: false, text: t("check_ds_unsigned") });
      }
      // What a validating resolver makes of it all
      if (!c.resolution) {
        lines.push({ ok: null, text: t("check_no_resolver") });
      } else {
        lines.push({
          ok: c.resolution === "ok",
          text: t("check_resolve_" + c.resolution, { resolver: c.resolver }),
        });
      }
      return lines;
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
        this.isAddShown = false;
        await this.load();
        // What to give the registrar comes next, so show it straight away
        await this.showDetails({ zone: out.zone });
      } catch (failure) {
        this.error.zone = this.taskErrorText(failure);
      }
      this.loading.add = false;
    },
    async showDetails(zone) {
      this.error.details = "";
      try {
        const info = await this.runTask("get-zone", { zone: zone.zone });
        this.details = { ...info, wasSigned: false };
        this.check = null;
      } catch (failure) {
        this.error.action = this.taskErrorText(failure);
      }
    },
    closeDetails() {
      this.details = null;
      this.check = null;
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
          confirmDisable: false,
        };
        this.check = null;
      } catch (failure) {
        this.error.details = this.taskErrorText(failure);
        this.details = { ...this.details, dnssec: wasEnabled };
      }
      this.loading.details = false;
    },
    isReverse(zone) {
      return /\.arpa\.?$/i.test(zone);
    },
    publicAddresses(ns) {
      return ns.addresses.filter((a) => a.public).map((a) => a.address);
    },
    async checkDelegation() {
      this.loading.check = true;
      this.error.details = "";
      try {
        this.check = await this.runTask("check-delegation", {
          zone: this.details.zone,
        });
      } catch (failure) {
        this.error.details = this.taskErrorText(failure);
      }
      this.loading.check = false;
    },
    async removeZone() {
      const zone = this.zoneToRemove.zone;
      this.zoneToRemove = null;
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
.registrar-title {
  margin-top: 1.5rem;
}
.registrar-intro {
  margin: 0.5rem 0;
}
h6 {
  margin-top: 1rem;
}
.check-button {
  margin-top: 1rem;
}
.check-line {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.check-line .bx--tag {
  flex-shrink: 0;
}
.check-delay {
  margin-top: 0.5rem;
  font-size: 0.875rem;
}
</style>
