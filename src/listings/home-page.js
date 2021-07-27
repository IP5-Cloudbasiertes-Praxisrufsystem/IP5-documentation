import {ApplicationSettings, Button, GridLayout} from "@nativescript/core";
import {MessageTrigger} from "~/components/message-trigger/message-trigger";
import { HomeItemsViewModel } from './home-model'
import {getClientConfiguration} from "~/services/configuration-api";
import {showError} from "~/error-dialog/error-dialog";

const model = new HomeItemsViewModel();
export function onPageLoaded(args){
    const mainComponent = args.object;
    mainComponent.bindingContext = model;
}

export function onGridLoaded(args){
    console.log("loading grid", ApplicationSettings.getString("clientId"))
    const grid = args.object;
    getClientConfiguration(ApplicationSettings.getString("clientId"))
        .then(result => buildMessageUI(result, grid))
        .catch((e) => showError("Loading Client Configuration failed", e, "OK"));
}

function buildMessageUI(clientConfiguration, grid){
    console.log("buildMessageUI",clientConfiguration)
    let rowCounter = 0;
    let columnCounter = 0;
    let rowIdx = 0;
    let columnIdx = 0;
    clientConfiguration.map((conf) => {
        const messageComp = new MessageTrigger(conf.title, conf.id);
        grid.addChild(messageComp);
        GridLayout.setRow(messageComp,rowIdx);
        GridLayout.setColumn(messageComp,columnIdx);
        rowCounter++
        columnCounter++
        if(columnCounter > 2){
            columnIdx = 0;
            columnCounter = 0;
        } else {
            columnIdx++;
        }
        if(rowCounter > 3){
            rowIdx++;
            rowCounter = 0;
        }else {
            rowCounter++
        }
    })
}
