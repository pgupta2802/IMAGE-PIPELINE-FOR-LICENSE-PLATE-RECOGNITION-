import axios from 'axios';

export default async function results(filename) {
    try {
        const response = await axios.get(
            'https://72gd4ty269.execute-api.ca-central-1.amazonaws.com/image',
            {params: { filename: filename }}
        );
        return response.data;
    } catch(e) {
        if (e.response && e.response.status === 404) {
            return null;
        }
        console.error(e.response.data);
        alert(error.response.data.error);
        throw e;
    }
}