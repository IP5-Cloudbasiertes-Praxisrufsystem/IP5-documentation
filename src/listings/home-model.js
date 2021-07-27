import {fromObject, Observable, ObservableArray} from '@nativescript/core'

export function HomeItemsViewModel() {
    const viewModel = new Observable();
    viewModel.set("newMessageTitle","");
    viewModel.notificationConfigurations = new ObservableArray([])

    return viewModel
}
