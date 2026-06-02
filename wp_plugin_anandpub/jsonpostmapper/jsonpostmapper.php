<?php
/**
 * Plugin Name: JSON Post Mapper
 * Description: A plugin to map JSON fields to custom post fields including ACF fields.
 * Version: 1.0
 * Author: Your Name
 */

// Hook for admin menu
add_action('admin_menu', 'json_to_custom_post_mapper_menu');

function json_to_custom_post_mapper_menu() {
    add_menu_page(
        'json to Custom Post Mapper',
        'json Mapper',
        'manage_options',
        'json-to-custom-post-mapper',
        'json_to_custom_post_mapper_page'
    );
}

function json_to_custom_post_mapper_page() {
    ?>
    <div class="wrap">
        <h1>json to Custom Post Mapper</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="json_file" accept=".json">
            <input type="submit" name="import_json" value="Import JSON" class="button-primary">
        </form>
        <?php
        if (isset($_POST['import_json'])) {
            json_to_custom_post_mapper_import();
        }
        ?>
    </div>
    <?php
}

function json_to_custom_post_mapper_import() {
    if (!isset($_FILES['json_file']) || $_FILES['json_file']['error'] !== UPLOAD_ERR_OK) {
        echo '<div class="error"><p>Error uploading file.</p></div>';
        return;
    }

    $file = $_FILES['json_file']['tmp_name'];
    $json_data = file_get_contents($file);

    // Decode the JSON into an associative array
    $data_array = json_decode($json_data, true);

    if ($data_array === null) {
        echo '<div class="error"><p>Invalid JSON file.</p></div>';
        return;
    }

    global $wpdb;
    $timestamp = strtotime('now'); // Start with current timestamp

    foreach ($data_array as $data) {
        // Process each JSON object as a custom post
        $post_data = array(
            'post_title'   => $data['title'],  // Adjust for your JSON structure
            'post_status'  => 'publish',
            'post_type'    => 'custom_post',  // Change to your custom post type
            'post_date'    => date('Y-m-d H:i:s', $timestamp)  // Set post date
        );

        if (empty($post_data['post_title'])) {
            continue; // Skip if title is empty
        }

        $post_id = wp_insert_post($post_data);

        if (is_wp_error($post_id)) {
            continue;
        }

        // Update ACF fields
        $acf_field_key_title_2 = 'title';
        $acf_field_key_content = 'content';

        // Updating the title_2 for preview of posts
        update_field($acf_field_key_title_2, $data['title_2'], $post_id);

        // Step 1: Insert trimmed content
        $trimmed_content = substr($data['content'], 0, 100); // Adjust trimming as necessary
        update_field($acf_field_key_content, $trimmed_content, $post_id);

        // Step 2: Get meta_id for the inserted ACF field
        $meta_id = $wpdb->get_var(
            $wpdb->prepare(
                "SELECT meta_id FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key LIKE '%content%'",
                $post_id
            )
        );

        echo "Meta ID = ". $meta_id;

        // Step 3: Replace trimmed content with original content directly in the database
        if ($meta_id) {
            $wpdb->update(
                $wpdb->postmeta,
                array('meta_value' => $data['content']),
                array('meta_id' => $meta_id),
                array('%s'),
                array('%d')
            );
        }

        // Step 4: Create or get category from 'archive_date'
        if (!empty($data['archive_date'])) {
            $archive_date_term = term_exists($data['archive_date'], 'archive');
            if ($archive_date_term === 0 || $archive_date_term === null) {
                // Term doesn't exist, so create it
                $archive_date_term = wp_insert_term($data['archive_date'], 'archive');
            }
            
            // Assign the archive date category to the post
            if (!is_wp_error($archive_date_term)) {
                wp_set_post_terms($post_id, array($archive_date_term['term_id']), 'archive');
            }
        }

        // Increment timestamp to ensure the next post has a later date
        $timestamp += 60; // Add 60 seconds (1 minute) to the timestamp for each post
    }

    echo '<div class="updated"><p>JSON imported successfully!</p></div>';
}
