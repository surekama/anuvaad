import C from "../constants";

export function currentPageUpdate(page_number) {
    console.log(page_number)
    return {     
        type: C.UPDATE_PAGENUMBER,
        
        payload: {
            page_number
        }
    }
}
