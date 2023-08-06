#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   Copyright 2018 Open Energy Efficiency, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
import statsmodels.formula.api as smf

from ..features import (
    compute_time_features,
    compute_temperature_bin_features,
    compute_occupancy_feature,
    merge_features,
)
from ..segmentation import SegmentModel, fit_segmented_model


__all__ = (
    "caltrack_hourly_fit_feature_processor",
    "caltrack_hourly_prediction_feature_processor",
    "fit_caltrack_hourly_model_segment",
    "fit_caltrack_hourly_model",
)


def caltrack_hourly_fit_feature_processor(
    segment_name, segmented_data, occupancy_lookup, temperature_bins
):
    # get occupied feature
    hour_of_week = segmented_data.hour_of_week
    occupancy = occupancy_lookup[segment_name]
    occupancy_feature = compute_occupancy_feature(hour_of_week, occupancy)

    # get temperature bin features
    temperatures = segmented_data.temperature_mean
    bin_endpoints_list = (
        temperature_bins[segment_name].index[temperature_bins[segment_name]].tolist()
    )
    temperature_bin_features = compute_temperature_bin_features(
        segmented_data.temperature_mean, bin_endpoints_list
    )

    # combine features
    return merge_features(
        [
            segmented_data[["meter_value", "hour_of_week"]],
            occupancy_feature,
            temperature_bin_features,
            segmented_data.weight,
        ]
    )


def caltrack_hourly_prediction_feature_processor(
    segment_name, segmented_data, occupancy_lookup, temperature_bins
):
    # hour of week feature
    hour_of_week_feature = compute_time_features(
        segmented_data.index, hour_of_week=True, day_of_week=False, hour_of_day=False
    )

    # occupancy feature
    occupancy = occupancy_lookup[segment_name]
    occupancy_feature = compute_occupancy_feature(
        hour_of_week_feature.hour_of_week, occupancy
    )

    # get temperature bin features
    temperatures = segmented_data
    bin_endpoints_list = (
        temperature_bins[segment_name].index[temperature_bins[segment_name]].tolist()
    )
    temperature_bin_features = compute_temperature_bin_features(
        segmented_data.temperature_mean, bin_endpoints_list
    )

    # combine features
    return merge_features(
        [
            hour_of_week_feature,
            occupancy_feature,
            temperature_bin_features,
            segmented_data.weight,
        ]
    )


def fit_caltrack_hourly_model_segment(segment_name, segment_data):
    def _get_hourly_model_formula(data):
        bin_occupancy_interactions = "".join(
            [" + {}:C(occupancy)".format(c) for c in data.columns if "bin" in c]
        )
        return "meter_value ~ C(hour_of_week) - 1{}".format(bin_occupancy_interactions)

    formula = _get_hourly_model_formula(segment_data)
    model = smf.wls(formula=formula, data=segment_data, weights=segment_data.weight)
    model_params = {coeff: value for coeff, value in model.fit().params.items()}
    warnings = []
    return SegmentModel(
        segment_name=segment_name,
        model=model,
        formula=formula,
        model_params=model_params,
        warnings=warnings,
    )


def fit_caltrack_hourly_model(
    segmented_design_matrices, occupancy_lookup, temperature_bins
):
    segmented_model = fit_segmented_model(
        segmented_design_matrices,
        fit_caltrack_hourly_model_segment,
        prediction_segment_type="one_month",
        prediction_segment_name_mapping={
            "jan": "dec-jan-feb-weighted",
            "feb": "jan-feb-mar-weighted",
            "mar": "feb-mar-apr-weighted",
            "apr": "mar-apr-may-weighted",
            "may": "apr-may-jun-weighted",
            "jun": "may-jun-jul-weighted",
            "jul": "jun-jul-aug-weighted",
            "aug": "jul-aug-sep-weighted",
            "sep": "aug-sep-oct-weighted",
            "oct": "sep-oct-nov-weighted",
            "nov": "oct-nov-dec-weighted",
            "dec": "nov-dec-jan-weighted",
        },
        prediction_feature_processor=caltrack_hourly_prediction_feature_processor,
        prediction_feature_processor_kwargs={
            "occupancy_lookup": occupancy_lookup,
            "temperature_bins": temperature_bins,
        },
    )
    return segmented_model
